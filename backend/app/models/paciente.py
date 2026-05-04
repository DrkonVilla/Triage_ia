from sqlalchemy import Column, String, Date, Integer
from sqlalchemy.orm import relationship
from app.models.base import BaseModel

class Paciente(BaseModel):
    __tablename__ = "pacientes"
    
    dni = Column(String(20), unique=True, nullable=False, index=True)
    nombres = Column(String(100), nullable=False)
    apellidos = Column(String(100), nullable=False)
    fecha_nacimiento = Column(Date, nullable=False)
    genero = Column(String(10))
    telefono = Column(String(20))
    email = Column(String(100))
    direccion = Column(String(255))
    
    # Relaciones
    contactos_emergencia = relationship("ContactoEmergencia", back_populates="paciente", cascade="all, delete-orphan")
    triajes = relationship("Triaje", back_populates="paciente", foreign_keys="Triaje.paciente_id")
    antecedentes = relationship("HCEAntecedente", back_populates="paciente", cascade="all, delete-orphan")
    consultas_previas = relationship("HCEConsultaPrevia", back_populates="paciente", cascade="all, delete-orphan")
    
    @property
    def edad(self):
        """Calcula edad actual"""
        from datetime import date
        today = date.today()
        return today.year - self.fecha_nacimiento.year - (
            (today.month, today.day) < (self.fecha_nacimiento.month, self.fecha_nacimiento.day)
        )