from typing import Optional, Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from jose import JWTError, jwt

from app.database import get_db
from app.config import settings
from app.models.usuario import Usuario
from app.schemas.usuario import TokenResponse

security = HTTPBearer()

async def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
    db: Annotated[AsyncSession, Depends(get_db)]
) -> Usuario:
    """Obtiene el usuario actual desde el token JWT"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciales inválidas",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        token = credentials.credentials
        payload = jwt.decode(
            token, 
            settings.SECRET_KEY, 
            algorithms=[settings.ALGORITHM]
        )
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    # Buscar usuario en BD
    result = await db.execute(
        select(Usuario).where(Usuario.username == username, Usuario.activo == True)
    )
    user = result.scalar_one_or_none()
    
    if user is None:
        raise credentials_exception
    
    return user

async def get_current_active_user(
    current_user: Annotated[Usuario, Depends(get_current_user)]
) -> Usuario:
    """Verifica que el usuario esté activo"""
    if not current_user.activo:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuario inactivo"
        )
    return current_user

def require_role(required_role: str):
    """Factory para dependencia de verificación de roles"""
    async def role_checker(
        current_user: Annotated[Usuario, Depends(get_current_active_user)]
    ) -> Usuario:
        if current_user.rol != required_role and current_user.rol != "gerente":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Se requiere rol '{required_role}' para esta operación"
            )
        return current_user
    return role_checker

# Tipos anotados para fácil uso
CurrentUser = Annotated[Usuario, Depends(get_current_active_user)]
EnfermeraDep = Annotated[Usuario, Depends(require_role("enfermera"))]
MedicoDep = Annotated[Usuario, Depends(require_role("medico"))]
GerenteDep = Annotated[Usuario, Depends(require_role("gerente"))]
AuditorDep = Annotated[Usuario, Depends(require_role("auditor"))]