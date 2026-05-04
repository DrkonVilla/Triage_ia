from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, case
from sqlalchemy.orm import selectinload
from typing import List, Optional
from datetime import datetime

from app.database import get_db
from app.dependencies import MedicoDep
from app.models.triaje import Triaje
from app.models.paciente import Paciente
from app.schemas.triaje import TriajeResponse, CambioEstadoRequest, EstadoLogistico
from app.services.audit_service import audit_log

router = APIRouter(prefix="/api/v1/cola-medica", tags=["Cola Médica"])

# Orden de prioridad para niveles de urgencia
URGENCY_ORDER = {
    "RED": 1,
    "ORANGE": 2,
    "YELLOW": 3,
    "GREEN": 4,
    "BLUE": 5
}

@router.get("/", response_model=List[TriajeResponse])
async def get_cola_medica(
    db: AsyncSession = Depends(get_db),
    current_user: MedicoDep = None,
    estado: Optional[str] = None
):
    """
    Obtiene cola médica ordenada por urgencia y antigüedad.
    Incluye últimos 5 atendidos del día.
    Solo para médicos.
    """
    from datetime import date
    
    # 1. Obtener pendientes
    query_pendientes = (
        select(Triaje, Paciente)
        .options(
            selectinload(Triaje.signos_vitales),
            selectinload(Triaje.sintomas),
            selectinload(Triaje.resultado_ia),
        )
        .join(Paciente, Triaje.paciente_id == Paciente.id)
        .where(
            Triaje.activo == True,
            Triaje.estado_logistico.in_(["En Espera", "Llamado", "En Atencion"])
        )
    )
    
    if estado and estado != "Atendido":
        query_pendientes = query_pendientes.where(Triaje.estado_logistico == estado)
    
    result_pendientes = await db.execute(query_pendientes)
    rows_pendientes = result_pendientes.all()
    
    # 2. Obtener últimos 5 atendidos del día
    hoy_inicio = datetime.combine(date.today(), datetime.min.time())
    hoy_fin = datetime.combine(date.today(), datetime.max.time())
    
    query_atendidos = (
        select(Triaje, Paciente)
        .options(
            selectinload(Triaje.signos_vitales),
            selectinload(Triaje.sintomas),
            selectinload(Triaje.resultado_ia),
        )
        .join(Paciente, Triaje.paciente_id == Paciente.id)
        .where(
            Triaje.activo == True,
            Triaje.estado_logistico == "Atendido",
            Triaje.updated_at >= hoy_inicio,
            Triaje.updated_at <= hoy_fin
        )
        .order_by(Triaje.updated_at.desc())
        .limit(5)
    )
    
    result_atendidos = await db.execute(query_atendidos)
    rows_atendidos = result_atendidos.all()
    
    # Combinar resultados
    all_rows = list(rows_pendientes) + list(rows_atendidos)
    
    # Procesar respuestas
    triajes = []
    for triaje, paciente in all_rows:
        triaje_response = TriajeResponse.model_validate(triaje)
        triaje_response.paciente_nombre_completo = f"{paciente.nombres} {paciente.apellidos}"
        triaje_response.paciente_edad = paciente.edad
        triajes.append(triaje_response)
    
    # Ordenar: nivel urgencia (RED > ORANGE > ...) y luego fecha_hora ASC
    # Atendidos van al final
    triajes.sort(key=lambda t: (
        0 if t.estado_logistico != "Atendido" else 1,  # Pendientes primero
        URGENCY_ORDER.get(t.nivel_urgencia_final, 99),
        t.fecha_hora
    ))
    
    return triajes

@router.put("/{triaje_id}/estado")
async def cambiar_estado(
    triaje_id: int,
    request: CambioEstadoRequest,
    db: AsyncSession = Depends(get_db),
    current_user: MedicoDep = None
):
    """
    Cambia estado logístico del triaje con control de concurrencia.
    Implementa máquina de estados estricta.
    """
    # Obtener triaje con versión actual
    result = await db.execute(
        select(Triaje).where(Triaje.id == triaje_id, Triaje.activo == True)
    )
    triaje = result.scalar_one_or_none()
    
    if not triaje:
        raise HTTPException(status_code=404, detail="Triaje no encontrado")
    
    # Validar transición según máquina de estados
    es_valido, mensaje = triaje.transicionar_estado(request.nuevo_estado.value, current_user.rol)
    if not es_valido:
        raise HTTPException(status_code=400, detail=mensaje)
    
    # Si es devolución a triaje, requiere justificación
    if request.nuevo_estado == EstadoLogistico.EN_ESPERA and triaje.estado_logistico == "Llamado":
        if not request.justificacion or len(request.justificacion) < 10:
            raise HTTPException(
                status_code=400,
                detail="Para devolver un paciente a triaje, debe proporcionar una justificación (mínimo 10 caracteres)"
            )
    
    # Guardar estado anterior para auditoría
    estado_anterior = triaje.estado_logistico
    version_actual = triaje.version
    
    # Registrar tiempo de atención si se finaliza
    tiempo_atencion = None
    if request.nuevo_estado == EstadoLogistico.ATENDIDO:
        if triaje.fecha_hora:
            delta = datetime.now() - triaje.fecha_hora
            tiempo_atencion = delta.total_seconds()
    
    # Ejecutar update con verificación de versión (optimistic locking)
    # Solo el UPDATE manual, NO modificar el objeto triaje antes
    stmt = update(Triaje).where(
        Triaje.id == triaje_id,
        Triaje.version == version_actual
    ).values(
        estado_logistico=request.nuevo_estado.value,
        version=Triaje.version + 1,
        tiempo_atencion_segundos=tiempo_atencion
    )
    
    result = await db.execute(stmt)
    if result.rowcount == 0:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="El registro fue modificado por otro médico. Por favor recargue la cola."
        )
    
    # Refrescar el objeto triaje para reflejar los cambios
    await db.refresh(triaje)
    
    await db.commit()
    
    # Auditoría con justificación si aplica
    detalles_extra = {}
    if request.justificacion:
        detalles_extra["justificacion"] = request.justificacion
    
    await audit_log(
        db, current_user.id, "STATUS_CHANGE", "estado_logistico", triaje_id,
        {"estado_anterior": estado_anterior},
        {"estado_nuevo": request.nuevo_estado.value, **detalles_extra}
    )
    
    return {
        "success": True,
        "message": f"Estado actualizado a {request.nuevo_estado.value}",
        "nuevo_estado": request.nuevo_estado.value,
        "version": triaje.version + 1
    }

@router.put("/{triaje_id}/notas-medicas")
async def agregar_notas_medicas(
    triaje_id: int,
    notas: str,
    diagnostico_final: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
    current_user: MedicoDep = None
):
    """Médico agrega notas clínicas y diagnóstico final"""
    result = await db.execute(
        select(Triaje).where(Triaje.id == triaje_id)
    )
    triaje = result.scalar_one_or_none()
    
    if not triaje:
        raise HTTPException(status_code=404, detail="Triaje no encontrado")
    
    # Solo permitir si está en atención
    if triaje.estado_logistico != "En Atencion":
        raise HTTPException(
            status_code=400,
            detail="Solo se pueden agregar notas médicas cuando el paciente está 'En Atencion'"
        )
    
    triaje.notas_medicas = notas
    if diagnostico_final:
        triaje.diagnostico_final_medico = diagnostico_final
    triaje.version += 1
    
    await db.commit()
    
    await audit_log(
        db, current_user.id, "UPDATE", "notas_medicas", triaje_id,
        None,
        {"notas": notas[:100], "diagnostico": diagnostico_final}
    )
    
    return {"success": True, "message": "Notas médicas guardadas"}