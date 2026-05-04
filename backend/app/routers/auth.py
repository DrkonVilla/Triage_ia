from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.dependencies import CurrentUser
from app.schemas.usuario import LoginRequest, TokenResponse, UsuarioResponse
from app.services.auth_service import auth_service

router = APIRouter(prefix="/api/v1/auth", tags=["Autenticación"])

@router.post("/login", response_model=TokenResponse)
async def login(
    login_data: LoginRequest,
    db: AsyncSession = Depends(get_db)
):
    """Login de usuario - retorna token JWT"""
    return await auth_service.login(db, login_data)

@router.post("/logout")
async def logout():
    """Logout (cliente debe eliminar token)"""
    return {"success": True, "message": "Sesión cerrada exitosamente"}

@router.get("/me", response_model=UsuarioResponse)
async def me(current_user: CurrentUser):
    """Retorna el usuario autenticado según el token JWT"""
    return UsuarioResponse.model_validate(current_user)