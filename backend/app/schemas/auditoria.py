from datetime import datetime
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field

class LogAuditoriaBase(BaseModel):
    accion: str
    modulo: str
    registro_id: int

class LogAuditoriaCreate(LogAuditoriaBase):
    usuario_id: Optional[int] = None
    datos_anteriores: Optional[Dict[str, Any]] = None
    datos_nuevos: Optional[Dict[str, Any]] = None
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None

class LogAuditoriaResponse(LogAuditoriaBase):
    id: int
    usuario_id: Optional[int]
    usuario_nombre: Optional[str] = None
    datos_anteriores: Optional[Dict[str, Any]] = None
    datos_nuevos: Optional[Dict[str, Any]] = None
    ip_address: Optional[str] = None
    timestamp: datetime
    
    class Config:
        from_attributes = True

class AuditStatsResponse(BaseModel):
    total_logs: int
    acciones_por_modulo: Dict[str, int]
    top_usuarios_activos: list
    ultima_semana: int