from datetime import datetime
from sqlalchemy import Column, Integer, DateTime, Boolean, func
from sqlalchemy.ext.declarative import declared_attr
from app.database import Base

class TimestampMixin:
    """Mixin para auditoría temporal"""
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)

class SoftDeleteMixin:
    """Mixin para borrado lógico"""
    activo = Column(Boolean, default=True, nullable=False)

class OptimisticLockMixin:
    """Mixin para control de concurrencia optimista"""
    version = Column(Integer, default=1, nullable=False)
    
    def increment_version(self):
        """Incrementa la versión antes de guardar"""
        self.version += 1

class BaseModel(Base, TimestampMixin, SoftDeleteMixin, OptimisticLockMixin):
    """Modelo base abstracto con todas las funcionalidades"""
    __abstract__ = True
    
    id = Column(Integer, primary_key=True, index=True)
    
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()