from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_
from sqlalchemy.orm import selectinload
from typing import Optional, List
from datetime import datetime

from app.database import get_db
from app.dependencies import EnfermeraDep, CurrentUser
from app.models.triaje import Triaje
from app.models.paciente import Paciente
from app.models.signos_vitales import SignosVitales
from app.models.sintoma_triaje import SintomaTriaje
from app.models.resultado_ia import ResultadoIA
from app.schemas.triaje import (
    TriajeCreate, TriajeUpdate, TriajeResponse,
    SignosVitalesCreate, SintomaTriajeCreate
)
from app.services.ia_service import IAService
from app.services.audit_service import audit_log
from app.services.webhook_service import send_critical_alert

router = APIRouter(prefix="/api/v1/triaje", tags=["Triaje"])
ia_service = IAService()

@router.post("/", response_model=TriajeResponse, status_code=status.HTTP_201_CREATED)
async def create_triaje(
    triaje_data: TriajeCreate,
    db: AsyncSession = Depends(get_db),
    current_user: EnfermeraDep = None
):
    """
    Crea un nuevo triaje con evaluación IA.
    Solo enfermeras pueden crear triajes.
    """
    # Verificar que el paciente existe
    result = await db.execute(
        select(Paciente).where(Paciente.id == triaje_data.paciente_id, Paciente.activo == True)
    )
    paciente = result.scalar_one_or_none()
    if not paciente:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")
    
    # Crear el triaje base
    triaje = Triaje(
        paciente_id=triaje_data.paciente_id,
        usuario_id=current_user.id,
        motivo_consulta=triaje_data.motivo_consulta,
        fecha_hora=datetime.now(),
        estado_logistico="En Espera"
    )
    db.add(triaje)
    await db.flush()  # Obtener el ID del triaje
    
    # Crear signos vitales
    signos_data = triaje_data.signos_vitales
    signos = SignosVitales(
        triaje_id=triaje.id,
        presion_sistolica=signos_data.presion_sistolica,
        presion_diastolica=signos_data.presion_diastolica,
        frecuencia_cardiaca=signos_data.frecuencia_cardiaca,
        frecuencia_respiratoria=signos_data.frecuencia_respiratoria,
        temperatura=signos_data.temperatura,
        saturacion_o2=signos_data.saturacion_o2,
        nota_suplementaria=signos_data.nota_suplementaria
    )
    db.add(signos)
    
    # Crear síntomas
    sintomas_list = []
    for s in triaje_data.sintomas:
        sintoma = SintomaTriaje(
            triaje_id=triaje.id,
            sintoma=s.sintoma,
            intensidad=s.intensidad,
            descripcion_libre=s.descripcion_libre
        )
        db.add(sintoma)
        sintomas_list.append({
            "sintoma": s.sintoma,
            "intensidad": s.intensidad,
            "descripcion": s.descripcion_libre
        })
    
    # Llamar al servicio de IA para evaluación
    try:
        respuesta_ia, metadata, latencia = await ia_service.evaluar_triaje(
            motivo_consulta=triaje_data.motivo_consulta,
            signos_vitales=signos_data,
            sintomas=sintomas_list,
            paciente=None  # Podemos agregar datos del paciente si es necesario
        )
        
        # Actualizar triaje con resultado de IA
        triaje.nivel_urgencia_asignado_ia = respuesta_ia.nivel_urgencia.value
        triaje.nivel_urgencia_final = respuesta_ia.nivel_urgencia.value  # Por defecto, validación médica puede cambiar
        
        # Guardar resultado IA en tabla
        resultado_ia = ResultadoIA(
            triaje_id=triaje.id,
            prompt_enviado=metadata.get("prompt", ""),
            respuesta_raw_llm=respuesta_ia.model_dump_json(),
            diagnosticos_json={"diagnosticos": respuesta_ia.diagnosticos},
            recomendaciones_json={"recomendaciones": respuesta_ia.recomendaciones},
            modelo_utilizado=metadata.get("modelo", "gpt-4"),
            latencia_segundos=latencia
        )
        db.add(resultado_ia)
        
    except Exception as e:
        # Si falla IA, crear triaje sin evaluación IA pero con mensaje de error
        import logging
        logger = logging.getLogger(__name__)
        error_msg = str(e)
        logger.error(f"Error en evaluación IA: {error_msg}")
        
        # Verificar si es error de API Key
        error_lower = error_msg.lower()
        if ("api key" in error_lower or 
            "authentication" in error_lower or 
            "authorized" in error_lower or
            "no configurada" in error_lower or  # Mensaje en español de nuestro servicio
            "api_key" in error_lower):
            logger.error("ERROR: API Key de OpenAI no configurada o invalida")
            triaje.nivel_urgencia_asignado_ia = "ERROR_API_KEY"
        else:
            triaje.nivel_urgencia_asignado_ia = None
        
        triaje.nivel_urgencia_final = None
        # Guardar el error en notas médicas para referencia
        triaje.notas_medicas = f"[ERROR IA: {error_msg[:100]}...]"
    
    # Enviar alerta crítica a n8n si nivel es RED u ORANGE
    if triaje.nivel_urgencia_final in ("RED", "ORANGE"):
        await send_critical_alert(
            triaje_id=triaje.id,
            paciente_nombre=f"{paciente.nombres} {paciente.apellidos}",
            nivel_urgencia=triaje.nivel_urgencia_final,
            motivo=triaje.motivo_consulta
        )
    
    await db.commit()
    
    # Recargar triaje con relaciones eager para evitar MissingGreenlet
    result = await db.execute(
        select(Triaje)
        .options(
            selectinload(Triaje.signos_vitales),
            selectinload(Triaje.sintomas),
            selectinload(Triaje.resultado_ia)
        )
        .where(Triaje.id == triaje.id)
    )
    triaje = result.scalar_one()
    
    # Auditoría
    await audit_log(
        db, current_user.id, "INSERT", "triaje", triaje.id,
        None, {"paciente_id": triaje.paciente_id, "motivo": triaje.motivo_consulta}
    )
    
    return TriajeResponse.model_validate(triaje)


@router.get("/{triaje_id}", response_model=TriajeResponse)
async def get_triaje(
    triaje_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: CurrentUser = None
):
    """Obtiene un triaje por ID con todas sus relaciones"""
    result = await db.execute(
        select(Triaje)
        .options(
            selectinload(Triaje.signos_vitales),
            selectinload(Triaje.sintomas),
            selectinload(Triaje.resultado_ia)
        )
        .where(Triaje.id == triaje_id, Triaje.activo == True)
    )
    triaje = result.scalar_one_or_none()
    
    if not triaje:
        raise HTTPException(status_code=404, detail="Triaje no encontrado")
    
    return TriajeResponse.model_validate(triaje)


@router.get("/paciente/{paciente_id}", response_model=List[TriajeResponse])
async def get_triajes_by_paciente(
    paciente_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: CurrentUser = None,
    limit: int = Query(10, ge=1, le=50)
):
    """Obtiene los triajes de un paciente específico"""
    result = await db.execute(
        select(Triaje)
        .options(
            selectinload(Triaje.signos_vitales),
            selectinload(Triaje.sintomas)
        )
        .where(Triaje.paciente_id == paciente_id, Triaje.activo == True)
        .order_by(Triaje.fecha_hora.desc())
        .limit(limit)
    )
    triajes = result.scalars().all()
    
    return [TriajeResponse.model_validate(t) for t in triajes]


@router.put("/{triaje_id}", response_model=TriajeResponse)
async def update_triaje(
    triaje_id: int,
    triaje_data: TriajeUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: CurrentUser = None
):
    """
    Actualiza un triaje (nivel de urgencia final, notas médicas, etc.)
    """
    result = await db.execute(
        select(Triaje).where(Triaje.id == triaje_id, Triaje.activo == True)
    )
    triaje = result.scalar_one_or_none()
    
    if not triaje:
        raise HTTPException(status_code=404, detail="Triaje no encontrado")
    
    # Guardar datos anteriores para auditoría
    datos_anteriores = {
        "nivel_urgencia_final": triaje.nivel_urgencia_final,
        "estado_logistico": triaje.estado_logistico,
        "notas_medicas": triaje.notas_medicas
    }
    
    # Actualizar campos
    update_data = triaje_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(triaje, field, value)
    
    triaje.version += 1
    await db.commit()
    
    # Recargar con eager loading para evitar MissingGreenlet
    result = await db.execute(
        select(Triaje)
        .options(
            selectinload(Triaje.signos_vitales),
            selectinload(Triaje.sintomas),
            selectinload(Triaje.resultado_ia)
        )
        .where(Triaje.id == triaje_id)
    )
    triaje = result.scalar_one()
    
    # Auditoría
    await audit_log(
        db, current_user.id, "UPDATE", "triaje", triaje.id,
        datos_anteriores, update_data
    )
    
    return TriajeResponse.model_validate(triaje)


@router.put("/{triaje_id}/confirmar", response_model=TriajeResponse)
async def confirmar_nivel_urgencia(
    triaje_id: int,
    nivel_final: str,
    db: AsyncSession = Depends(get_db),
    current_user: CurrentUser = None
):
    """
    Confirma o sobreescribe el nivel de urgencia final del triaje.
    Actualiza el estado logístico a 'En Espera' para la cola médica.
    """
    result = await db.execute(
        select(Triaje).where(Triaje.id == triaje_id, Triaje.activo == True)
    )
    triaje = result.scalar_one_or_none()
    
    if not triaje:
        raise HTTPException(status_code=404, detail="Triaje no encontrado")
    
    # Guardar datos anteriores para auditoría
    datos_anteriores = {
        "nivel_urgencia_final": triaje.nivel_urgencia_final,
        "estado_logistico": triaje.estado_logistico
    }
    
    # Actualizar nivel final y estado
    triaje.nivel_urgencia_final = nivel_final
    triaje.estado_logistico = "En Espera"
    triaje.version += 1
    
    await db.commit()
    
    # Recargar con eager loading
    result = await db.execute(
        select(Triaje)
        .options(
            selectinload(Triaje.signos_vitales),
            selectinload(Triaje.sintomas),
            selectinload(Triaje.resultado_ia)
        )
        .where(Triaje.id == triaje_id)
    )
    triaje = result.scalar_one()
    
    # Auditoría
    await audit_log(
        db, current_user.id, "UPDATE", "triaje", triaje.id,
        datos_anteriores, {"nivel_urgencia_final": nivel_final, "estado_logistico": "En Espera"}
    )
    
    return TriajeResponse.model_validate(triaje)