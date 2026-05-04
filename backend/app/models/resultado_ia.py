from sqlalchemy import Column, Integer, String, Text, ForeignKey, Numeric
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSONB
from app.models.base import BaseModel

class ResultadoIA(BaseModel):
    __tablename__ = "resultados_ia"
    
    triaje_id = Column(Integer, ForeignKey("triajes.id"), unique=True, nullable=False)
    prompt_enviado = Column(Text, nullable=False)
    respuesta_raw_llm = Column(Text, nullable=False)
    diagnosticos_json = Column(JSONB)
    recomendaciones_json = Column(JSONB)
    modelo_utilizado = Column(String(50))
    latencia_segundos = Column(Numeric(5,2))
    
    triaje = relationship("Triaje", back_populates="resultado_ia")