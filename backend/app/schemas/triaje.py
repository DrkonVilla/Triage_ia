from pydantic import BaseModel, Field, field_validator
from typing import Optional, List, Literal
from datetime import datetime
from enum import Enum
from app.schemas.base import BaseSchema

# Enums para valores controlados
class NivelUrgencia(str, Enum):
    RED = "RED"  # Crítico / Reanimación
    ORANGE = "ORANGE"  # Urgente
    YELLOW = "YELLOW"  # Poco urgente
    GREEN = "GREEN"  # No urgente
    BLUE = "BLUE"  # Consulta administrativa

class EstadoLogistico(str, Enum):
    EN_ESPERA = "En Espera"
    LLAMADO = "Llamado"
    EN_ATENCION = "En Atencion"
    ATENDIDO = "Atendido"

class IntensidadSintoma(str, Enum):
    LEVE = "Leve"
    MODERADO = "Moderado"
    GRAVE = "Grave"

# Esquemas de Signos Vitales
class SignosVitalesBase(BaseSchema):
    presion_sistolica: Optional[int] = Field(None, ge=50, le=250)
    presion_diastolica: Optional[int] = Field(None, ge=30, le=200)
    frecuencia_cardiaca: Optional[int] = Field(None, ge=30, le=250)
    frecuencia_respiratoria: Optional[int] = Field(None, ge=5, le=60)
    temperatura: Optional[float] = Field(None, ge=30, le=45)
    saturacion_o2: Optional[int] = Field(None, ge=0, le=100)
    nota_suplementaria: Optional[str] = None

class SignosVitalesCreate(SignosVitalesBase):
    pass

class SignosVitalesResponse(SignosVitalesBase):
    id: int
    
    @field_validator('temperatura', mode='before')
    def parse_temperatura(cls, v):
        return float(v) if v else None

# Esquemas de Síntomas
class SintomaTriajeBase(BaseSchema):
    sintoma: str = Field(..., max_length=100)
    intensidad: Optional[IntensidadSintoma] = None
    descripcion_libre: Optional[str] = None

class SintomaTriajeCreate(SintomaTriajeBase):
    pass

class SintomaTriajeResponse(SintomaTriajeBase):
    id: int

# ESQUEMA DE RESPUESTA DEL LLM (Estructura validada estrictamente)
class DiagnosticoIA(BaseSchema):
    diagnostico_principal: str = Field(..., description="Diagnóstico principal sugerido")
    diferenciales: List[str] = Field(default_factory=list, description="Diagnósticos diferenciales")
    certeza: Optional[str] = Field(None, description="Alta/Media/Baja")

class RecomendacionIA(BaseSchema):
    conducta_inmediata: str = Field(..., description="Acción inmediata sugerida")
    estudios: Optional[str] = Field(None, description="Estudios complementarios")
    observaciones: Optional[str] = Field(None, description="Notas adicionales")

class RespuestaLlamaJSON(BaseSchema):
    """Estructura que DEBE devolver el LLM - Validación estricta"""
    nivel_urgencia: NivelUrgencia = Field(..., description="Nivel asignado según criterios Manchester")
    diagnosticos: List[str] = Field(default_factory=list, description="Lista de diagnósticos posibles")
    recomendaciones: str = Field(..., description="Recomendación conductual resumida")
    signos_alarma: List[str] = Field(default_factory=list, description="Signos de alarma identificados")
    requiere_aislamiento: bool = Field(default=False, description="Síntomas infecciosos")
    
    @field_validator('nivel_urgencia')
    def validate_urgency_rules(cls, v, values):
        """Validación adicional basada en reglas clínicas duras"""
        # Nota: Las reglas hard-coded están en el prompt, aquí solo estructura
        return v

# Esquema principal de Triaje
class TriajeBase(BaseSchema):
    paciente_id: int
    motivo_consulta: str = Field(..., min_length=5, max_length=500)
    nivel_urgencia_asignado_ia: Optional[NivelUrgencia] = None
    nivel_urgencia_final: Optional[NivelUrgencia] = None
    estado_logistico: EstadoLogistico = EstadoLogistico.EN_ESPERA

class TriajeCreate(TriajeBase):
    signos_vitales: SignosVitalesCreate
    sintomas: List[SintomaTriajeCreate] = Field(default_factory=list)
    
class TriajeUpdate(BaseSchema):
    nivel_urgencia_final: Optional[NivelUrgencia] = None
    estado_logistico: Optional[EstadoLogistico] = None
    notas_medicas: Optional[str] = None
    diagnostico_final_medico: Optional[str] = None

class CambioEstadoRequest(BaseSchema):
    nuevo_estado: EstadoLogistico
    justificacion: Optional[str] = Field(None, max_length=500)
    version_actual: int  # Para optimistic locking

class TriajeResponse(TriajeBase):
    id: int
    usuario_id: int
    fecha_hora: datetime
    notas_medicas: Optional[str]
    diagnostico_final_medico: Optional[str]
    tiempo_atencion_segundos: Optional[int]
    activo: bool
    version: int
    created_at: datetime
    updated_at: datetime
    
    # Relaciones anidadas
    signos_vitales: Optional[SignosVitalesResponse]
    sintomas: List[SintomaTriajeResponse] = []
    
    # Datos de paciente (para vistas de cola)
    paciente_nombre_completo: Optional[str] = None
    paciente_edad: Optional[int] = None
    
    class Config:
        from_attributes = True