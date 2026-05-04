from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, JSON, func
from sqlalchemy.dialects.postgresql import JSONB, INET
from sqlalchemy.orm import relationship
from app.database import Base

class LogAuditoria(Base):
    __tablename__ = "logs_auditoria"
    
    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=True)
    accion = Column(String(20), nullable=False)
    modulo = Column(String(50), nullable=False)
    registro_id = Column(Integer, nullable=False)
    datos_anteriores = Column(JSONB, nullable=True)
    datos_nuevos = Column(JSONB, nullable=True)
    ip_address = Column(INET, nullable=True)
    user_agent = Column(Text, nullable=True)
    timestamp = Column(DateTime, server_default=func.now(), nullable=False)
    
    # Relaciones
    usuario = relationship("Usuario", back_populates="logs_auditoria")
    
    def __repr__(self):
        return f"<LogAuditoria {self.accion} {self.modulo}:{self.registro_id}>"