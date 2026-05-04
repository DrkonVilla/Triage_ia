from datetime import date, datetime
from typing import Optional, List
from pydantic import BaseModel

class HCEAntecedenteBase(BaseModel):
    tipo: str  # Alergia, Patologia, Cirugia, Medicamento
    nombre: str
    descripcion: Optional[str] = None
    fecha_diagnostico: Optional[date] = None

class HCEAntecedenteCreate(HCEAntecedenteBase):
    pass

class HCEAntecedenteResponse(HCEAntecedenteBase):
    id: int
    activo: bool
    
    class Config:
        from_attributes = True

class HCEConsultaPreviaBase(BaseModel):
    fecha_consulta: datetime
    motivo: Optional[str] = None
    diagnostico_medico: Optional[str] = None
    tratamiento: Optional[str] = None

class HCEConsultaPreviaResponse(HCEConsultaPreviaBase):
    id: int
    
    class Config:
        from_attributes = True

class HCEAntecedentesResponse(BaseModel):
    paciente_id: int
    antecedentes: List[HCEAntecedenteResponse] = []
    consultas_previas: List[HCEConsultaPreviaResponse] = []

class FHIRResponse(BaseModel):
    resourceType: str
    type: str
    total: int
    entry: List[dict]