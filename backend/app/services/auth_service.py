from datetime import datetime, timedelta
from typing import Optional
from jose import jwt
import bcrypt
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.config import settings
from app.models.usuario import Usuario
from app.schemas.usuario import LoginRequest, TokenResponse, UsuarioResponse


class AuthService:
    """Servicio de autenticación y gestión de usuarios"""
    
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        # bcrypt tiene límite de 72 bytes
        if not plain_password or not hashed_password:
            return False

        plain_password_bytes = plain_password[:72].encode('utf-8')
        hashed_password_bytes = hashed_password.encode('utf-8')
        try:
            return bcrypt.checkpw(plain_password_bytes, hashed_password_bytes)
        except ValueError:
            # Hash inválido en BD (p.ej. "Invalid salt") => tratar como credenciales inválidas
            return False
    
    @staticmethod
    def get_password_hash(password: str) -> str:
        # bcrypt tiene límite de 72 bytes
        password = password[:72].encode('utf-8')
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password, salt).decode('utf-8')
    
    @staticmethod
    def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        return encoded_jwt
    
    @staticmethod
    async def authenticate_user(db: AsyncSession, username: str, password: str) -> Optional[Usuario]:
        """Autentica credenciales y retorna usuario si es válido"""
        username = (username or "").strip()
        result = await db.execute(
            select(Usuario).where(Usuario.username == username, Usuario.activo == True)
        )
        user = result.scalar_one_or_none()
        
        if not user:
            return None
        if not AuthService.verify_password(password, user.hashed_password):
            return None
        
        # Actualizar last_login
        user.last_login = datetime.utcnow()
        await db.commit()
        
        return user
    
    @staticmethod
    async def login(db: AsyncSession, login_data: LoginRequest) -> TokenResponse:
        """Procesa login y retorna token JWT"""
        user = await AuthService.authenticate_user(db, login_data.username, login_data.password)
        if not user:
            raise HTTPException(
                status_code=401,
                detail="Usuario o contraseña incorrectos",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        access_token = AuthService.create_access_token(data={"sub": user.username})
        
        return TokenResponse(
            access_token=access_token,
            token_type="bearer",
            expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            user=UsuarioResponse.model_validate(user)
        )

auth_service = AuthService()