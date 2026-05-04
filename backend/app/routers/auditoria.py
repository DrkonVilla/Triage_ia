from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import List, Optional
from datetime import datetime, timedelta

from app.database import get_db
from app.dependencies import AuditorDep, GerenteDep
from app.models.logs_auditoria import LogAuditoria
from app.models.usuario import Usuario
from app.schemas.auditoria import LogAuditoriaResponse

router = APIRouter(prefix="/api/v1/auditoria", tags=["Auditoría"])

@router.get("/logs", response_model=List[LogAuditoriaResponse])
async def get_logs_auditoria(
    db: AsyncSession = Depends(get_db),
    current_user: AuditorDep = None,
    modulo: Optional[str] = Query(None),
    usuario_id: Optional[int] = Query(None),
    desde: Optional[datetime] = Query(None),
    hasta: Optional[datetime] = Query(None),
    limit: int = Query(100, ge=1, le=500),
    offset: int = Query(0, ge=0)
):
    """Consulta logs de auditoría (solo auditores y gerentes)"""
    query = select(LogAuditoria, Usuario).join(
        Usuario, LogAuditoria.usuario_id == Usuario.id, isouter=True
    )
    
    if modulo:
        query = query.where(LogAuditoria.modulo == modulo)
    if usuario_id:
        query = query.where(LogAuditoria.usuario_id == usuario_id)
    if desde:
        query = query.where(LogAuditoria.timestamp >= desde)
    if hasta:
        query = query.where(LogAuditoria.timestamp <= hasta)
    
    query = query.order_by(LogAuditoria.timestamp.desc()).offset(offset).limit(limit)
    
    result = await db.execute(query)
    rows = result.all()
    
    logs = []
    for log, usuario in rows:
        # Convertir datos para manejar tipos inconsistentes en BD
        log_dict = {
            "id": log.id,
            "accion": log.accion,
            "modulo": log.modulo,
            "registro_id": log.registro_id,
            "usuario_id": log.usuario_id,
            "timestamp": log.timestamp,
            "user_agent": log.user_agent,
        }
        
        # Manejar datos_anteriores que pueden ser string o dict
        if log.datos_anteriores:
            if isinstance(log.datos_anteriores, str):
                log_dict["datos_anteriores"] = {"valor": log.datos_anteriores}
            else:
                log_dict["datos_anteriores"] = log.datos_anteriores
        else:
            log_dict["datos_anteriores"] = None
            
        # Manejar datos_nuevos que pueden ser string o dict
        if log.datos_nuevos:
            if isinstance(log.datos_nuevos, str):
                log_dict["datos_nuevos"] = {"valor": log.datos_nuevos}
            else:
                log_dict["datos_nuevos"] = log.datos_nuevos
        else:
            log_dict["datos_nuevos"] = None
            
        # Convertir ip_address INET a string
        if log.ip_address:
            log_dict["ip_address"] = str(log.ip_address)
        else:
            log_dict["ip_address"] = None
        
        log_response = LogAuditoriaResponse.model_validate(log_dict)
        if usuario:
            log_response.usuario_nombre = f"{usuario.nombres} {usuario.apellidos}" if usuario.nombres else usuario.username
        logs.append(log_response)
    
    return logs

@router.get("/stats")
async def get_audit_stats(
    db: AsyncSession = Depends(get_db),
    current_user: GerenteDep = None
):
    """Estadísticas de auditoría para gerencia"""
    # Total de acciones por módulo
    result = await db.execute(
        select(LogAuditoria.modulo, func.count()).group_by(LogAuditoria.modulo)
    )
    acciones_por_modulo = {row[0]: row[1] for row in result.all()}
    
    # Top 5 usuarios más activos
    result = await db.execute(
        select(LogAuditoria.usuario_id, func.count())
        .where(LogAuditoria.usuario_id.isnot(None))
        .group_by(LogAuditoria.usuario_id)
        .order_by(func.count().desc())
        .limit(5)
    )
    top_usuarios = [{"usuario_id": row[0], "acciones": row[1]} for row in result.all()]
    
    return {
        "total_logs": await db.scalar(select(func.count()).select_from(LogAuditoria)),
        "acciones_por_modulo": acciones_por_modulo,
        "top_usuarios_activos": top_usuarios,
        "ultima_semana": await db.scalar(
            select(func.count()).where(
                LogAuditoria.timestamp >= datetime.now().replace(hour=0, minute=0, second=0) - timedelta(days=7)
            )
        )
    }