from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import BaseModel

class ContactoEmergencia(BaseModel):
    __tablename__ = "contactos_emergencia"
    
    paciente_id = Column(Integer, ForeignKey("pacientes.id"), nullable=False)
    nombres_completos = Column(String(150), nullable=False)
    telefono = Column(String(20), nullable=False)
    parentesco = Column(String(50))
    
    paciente = relationship("Paciente", back_populates="contactos_emergencia")