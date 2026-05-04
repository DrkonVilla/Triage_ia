from sqlalchemy import Column, String, DateTime, Boolean
from sqlalchemy.orm import relationship
from app.models.base import BaseModel

class Usuario(BaseModel):
    __tablename__ = "usuarios"
    
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(100), unique=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    nombres = Column(String(100))
    apellidos = Column(String(100))
    rol = Column(String(20), nullable=False)  # enfermera, medico, gerente, auditor
    last_login = Column(DateTime)
    
    # Relaciones
    triajes = relationship("Triaje", back_populates="usuario", foreign_keys="Triaje.usuario_id")
    logs_auditoria = relationship("LogAuditoria", back_populates="usuario")
    
    def __repr__(self):
        return f"<Usuario {self.username} ({self.rol})>"