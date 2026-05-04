from sqlalchemy import Column, Integer, String, Text, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import BaseModel

class HCEAntecedente(BaseModel):
    __tablename__ = "hce_antecedentes"
    
    paciente_id = Column(Integer, ForeignKey("pacientes.id"), nullable=False)
    tipo = Column(String(50), nullable=False)
    nombre = Column(String(150), nullable=False)
    descripcion = Column(Text)
    fecha_diagnostico = Column(Date)
    activo = Column(default=True)
    
    paciente = relationship("Paciente", back_populates="antecedentes")