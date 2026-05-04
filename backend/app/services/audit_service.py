from sqlalchemy.ext.asyncio import AsyncSession
from app.models.logs_auditoria import LogAuditoria
from fastapi import Request

async def audit_log(
    db: AsyncSession,
    usuario_id: int,
    accion: str,
    modulo: str,
    registro_id: int,
    datos_anteriores: dict = None,
    datos_nuevos: dict = None,
    request: Request = None
):
    """Registra acción en log de auditoría"""
    log = LogAuditoria(
        usuario_id=usuario_id,
        accion=accion,
        modulo=modulo,
        registro_id=registro_id,
        datos_anteriores=datos_anteriores if datos_anteriores else None,
        datos_nuevos=datos_nuevos if datos_nuevos else None,
        ip_address=request.client.host if request else None,
        user_agent=request.headers.get("user-agent") if request else None
    )
    db.add(log)
    await db.flush()
