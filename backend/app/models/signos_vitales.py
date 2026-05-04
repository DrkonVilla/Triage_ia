from sqlalchemy import Column, Integer, Numeric, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import BaseModel

class SignosVitales(BaseModel):
    __tablename__ = "signos_vitales"
    
    triaje_id = Column(Integer, ForeignKey("triajes.id"), unique=True, nullable=False)
    presion_sistolica = Column(Integer)
    presion_diastolica = Column(Integer)
    frecuencia_cardiaca = Column(Integer)
    frecuencia_respiratoria = Column(Integer)
    temperatura = Column(Numeric(4,1))
    saturacion_o2 = Column(Integer)
    nota_suplementaria = Column(Text)
    
    triaje = relationship("Triaje", back_populates="signos_vitales")