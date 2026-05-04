from pydantic import BaseModel, Field, EmailStr, field_validator
from typing import Optional
from datetime import datetime
from app.schemas.base import BaseSchema

class UsuarioBase(BaseSchema):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    nombres: Optional[str] = Field(None, max_length=100)
    apellidos: Optional[str] = Field(None, max_length=100)
    rol: str = Field(..., pattern="^(enfermera|medico|gerente|auditor)$")

class UsuarioCreate(UsuarioBase):
    password: str = Field(..., min_length=8)
    
    @field_validator('password')
    def validate_password(cls, v):
        if not any(c.isupper() for c in v):
            raise ValueError('La contraseña debe contener al menos una mayúscula')
        if not any(c.isdigit() for c in v):
            raise ValueError('La contraseña debe contener al menos un número')
        return v

class UsuarioUpdate(BaseSchema):
    nombres: Optional[str] = None
    apellidos: Optional[str] = None
    email: Optional[EmailStr] = None
    activo: Optional[bool] = None

class UsuarioResponse(UsuarioBase):
    id: int
    activo: bool
    last_login: Optional[datetime]
    created_at: datetime
    version: int

class LoginRequest(BaseSchema):
    username: str
    password: str

class TokenResponse(BaseSchema):
    access_token: str
    token_type: str = "bearer"
    expires_in: int
    user: UsuarioResponse