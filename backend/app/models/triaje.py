from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.models.base import BaseModel

class Triaje(BaseModel):
    __tablename__ = "triajes"
    
    paciente_id = Column(Integer, ForeignKey("pacientes.id"), nullable=False)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    fecha_hora = Column(DateTime, nullable=False)
    motivo_consulta = Column(Text, nullable=False)
    nivel_urgencia_asignado_ia = Column(String(10))
    nivel_urgencia_final = Column(String(10))
    estado_logistico = Column(String(20), default="En Espera")
    notas_medicas = Column(Text)
    diagnostico_final_medico = Column(Text)
    tiempo_atencion_segundos = Column(Integer)
    sincronizado_hce = Column(Boolean, default=False, nullable=False)
    fecha_sincronizacion_hce = Column(DateTime, nullable=True)
    
    # Relaciones
    paciente = relationship("Paciente", back_populates="triajes", foreign_keys=[paciente_id])
    usuario = relationship("Usuario", back_populates="triajes", foreign_keys=[usuario_id])
    signos_vitales = relationship("SignosVitales", back_populates="triaje", uselist=False, cascade="all, delete-orphan")
    sintomas = relationship("SintomaTriaje", back_populates="triaje", cascade="all, delete-orphan")
    resultado_ia = relationship("ResultadoIA", back_populates="triaje", uselist=False, cascade="all, delete-orphan")
    
    def transicionar_estado(self, nuevo_estado: str, usuario_rol: str):
        """
        Valida y ejecuta transición de estado según rol
        Retorna tuple (bool, mensaje_error)
        """
        transiciones_validas = {
            "En Espera": ["Llamado"],
            "Llamado": ["En Atencion", "En Espera"],  # Devolver a triaje permitido
            "En Atencion": ["Atendido"],
            "Atendido": []  # Estado terminal
        }
        
        if nuevo_estado not in transiciones_validas.get(self.estado_logistico, []):
            return False, f"Transición inválida: {self.estado_logistico} -> {nuevo_estado}"
        
        # Reglas específicas por rol
        if usuario_rol == "medico":
            if nuevo_estado == "En Espera" and self.estado_logistico == "Llamado":
                # Devolver a triaje requiere justificación (se maneja en servicio)
                return True, "Requiere justificación"
            return True, ""
        else:
            return False, "Solo médicos pueden cambiar estados logísticos"

