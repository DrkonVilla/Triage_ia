from sqlalchemy import Column, Integer, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import BaseModel

class HCEConsultaPrevia(BaseModel):
    __tablename__ = "hce_consulta_previa"
    
    paciente_id = Column(Integer, ForeignKey("pacientes.id"), nullable=False)
    fecha_consulta = Column(DateTime, nullable=False)
    motivo = Column(Text)
    diagnostico_medico = Column(Text)
    tratamiento = Column(Text)
    
    paciente = relationship("Paciente", back_populates="consultas_previas")