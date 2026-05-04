from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime
from typing import Dict, Any

from app.database import get_db
from app.dependencies import CurrentUser
from app.models.paciente import Paciente
from app.models.hce_antecedentes import HCEAntecedente
from app.models.hce_consulta_previa import HCEConsultaPrevia
from app.schemas.hce import HCEAntecedentesResponse, FHIRResponse

router = APIRouter(prefix="/api/v1/hce", tags=["HCE"])

@router.get("/{paciente_id}", response_model=FHIRResponse)
async def get_antecedentes_hce(
    paciente_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: CurrentUser = None
) -> Dict[str, Any]:
    """Simula integración con HCE externa - Formato FHIR"""
    
    # Verificar paciente existe
    result = await db.execute(
        select(Paciente).where(Paciente.id == paciente_id, Paciente.activo == True)
    )
    paciente = result.scalar_one_or_none()
    if not paciente:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")
    
    # Obtener antecedentes
    result = await db.execute(
        select(HCEAntecedente).where(
            HCEAntecedente.paciente_id == paciente_id,
            HCEAntecedente.activo == True
        ).limit(20)
    )
    antecedentes = result.scalars().all()
    
    # Obtener consultas previas
    result = await db.execute(
        select(HCEConsultaPrevia).where(
            HCEConsultaPrevia.paciente_id == paciente_id
        ).order_by(HCEConsultaPrevia.fecha_consulta.desc()).limit(10)
    )
    consultas = result.scalars().all()
    
    # Construir respuesta FHIR
    entry = []
    
    for ant in antecedentes:
        entry.append({
            "resource": {
                "resourceType": "Condition",
                "code": {"coding": [{"code": ant.tipo, "display": ant.nombre}]},
                "category": {"text": ant.tipo},
                "recordedDate": ant.fecha_diagnostico.isoformat() if ant.fecha_diagnostico else None,
                "note": [{"text": ant.descripcion}] if ant.descripcion else []
            }
        })
    
    for cons in consultas:
        entry.append({
            "resource": {
                "resourceType": "Encounter",
                "period": {"start": cons.fecha_consulta.isoformat()},
                "reasonCode": [{"text": cons.motivo}] if cons.motivo else [],
                "diagnosis": [{"conditionDisplay": cons.diagnostico_medico}] if cons.diagnostico_medico else []
            }
        })
    
    return {
        "resourceType": "Bundle",
        "type": "searchset",
        "total": len(entry),
        "entry": entry
    }

@router.post("/{paciente_id}/sync")
async def sync_to_hce(
    paciente_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: CurrentUser = None
):
    """Simula sincronización con HCE externa"""
    
    result = await db.execute(
        select(Paciente).where(Paciente.id == paciente_id)
    )
    paciente = result.scalar_one_or_none()
    
    if not paciente:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")
    
    # Simular envío exitoso
    return {
        "success": True,
        "message": f"Datos del paciente {paciente.dni} sincronizados con HCE",
        "timestamp": datetime.now().isoformat()
    }