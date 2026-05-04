from pydantic import BaseModel, Field, field_validator
from typing import Optional, List
from datetime import date, datetime
from app.schemas.base import BaseSchema

class ContactoEmergenciaBase(BaseSchema):
    nombres_completos: str = Field(..., max_length=150)
    telefono: str = Field(..., max_length=20)
    parentesco: Optional[str] = Field(None, max_length=50)

class ContactoEmergenciaCreate(ContactoEmergenciaBase):
    pass

class ContactoEmergenciaResponse(ContactoEmergenciaBase):
    id: int

class PacienteBase(BaseSchema):
    dni: str = Field(..., min_length=6, max_length=20)
    nombres: str = Field(..., max_length=100)
    apellidos: str = Field(..., max_length=100)
    fecha_nacimiento: date
    genero: Optional[str] = Field(None, pattern="^(M|F|Otros)$")
    telefono: Optional[str] = Field(None, max_length=20)
    email: Optional[str] = None
    direccion: Optional[str] = None

class PacienteCreate(PacienteBase):
    contactos_emergencia: Optional[List[ContactoEmergenciaCreate]] = []

class PacienteUpdate(BaseSchema):
    nombres: Optional[str] = None
    apellidos: Optional[str] = None
    telefono: Optional[str] = None
    email: Optional[str] = None
    direccion: Optional[str] = None
    activo: Optional[bool] = None

class PacienteResponse(PacienteBase):
    id: int
    edad: int
    activo: bool
    created_at: datetime
    updated_at: datetime
    version: int
    contactos_emergencia: List[ContactoEmergenciaResponse] = []