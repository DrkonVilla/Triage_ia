from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
import os
from dotenv import load_dotenv

load_dotenv()

# Configuración PostgreSQL async
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+asyncpg://triaje_user:triaje_pass@localhost:5432/triaje_db"
)

engine = create_async_engine(
    DATABASE_URL,
    echo=True,  # Set False en producción
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True  # Verifica conexiones rotas
)

AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

Base = declarative_base()

async def get_db():
    """Dependencia para obtener sesión de DB"""
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

# Función para inicializar la base de datos (usar solo en setup)
async def init_db():
    async with engine.begin() as conn:
        # Importar todos los modelos aquí para que Base los registre
        from app.models.usuario import Usuario
        from app.models.paciente import Paciente
        from app.models.triaje import Triaje
        from app.models.signos_vitales import SignosVitales
        from app.models.sintoma_triaje import SintomaTriaje
        from app.models.resultado_ia import ResultadoIA
        from app.models.logs_auditoria import LogAuditoria
        
        # Crear todas las tablas
        await conn.run_sync(Base.metadata.create_all)