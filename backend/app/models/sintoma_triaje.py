from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import BaseModel

class SintomaTriaje(BaseModel):
    __tablename__ = "sintomas_triaje"
    
    triaje_id = Column(Integer, ForeignKey("triajes.id"), nullable=False)
    sintoma = Column(String(100), nullable=False)
    intensidad = Column(String(20))
    descripcion_libre = Column(Text)
    
    triaje = relationship("Triaje", back_populates="sintomas")