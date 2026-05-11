from fastapi import FastAPI, HTTPException, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
import logging
from datetime import datetime
import httpx
import os

from app.routers import auth, pacientes, triaje, cola_medica, hce, auditoria, reportes
from app.database import engine, Base
from app.config import settings

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Sistema de Triaje Clínico Asistido por IA",
    version="1.0.0",
    description="API para gestión de triaje con soporte de IA y control de concurrencia",
    docs_url="/docs",
    redoc_url="/redoc"
)

# ============================================
# CORS - Configuración CORREGIDA
# ============================================
# Obtener orígenes permitidos desde variable de entorno o usar lista por defecto
ALLOWED_ORIGINS = os.getenv(
    "ALLOWED_ORIGINS",
    "https://triage-streamlit-production.up.railway.app,https://triageiaxd.vercel.app,http://localhost:8501,http://localhost:5173,http://localhost:8000"
).split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,  # Lista específica, no "*"
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

# ============================================
# Routers
# ============================================
app.include_router(auth.router)
app.include_router(pacientes.router)
app.include_router(triaje.router)
app.include_router(cola_medica.router)
app.include_router(hce.router)
app.include_router(auditoria.router)
app.include_router(reportes.router)

# ============================================
# Endpoints públicos
# ============================================

@app.get("/")
async def root():
    """Endpoint raíz - información básica del sistema"""
    return {
        "name": "Sistema de Triaje Clínico Asistido por IA",
        "version": "1.0.0",
        "status": "operational",
        "docs_url": "/docs",
        "health_url": "/health"
    }

@app.get("/health")
async def health_check():
    """Health check para Railway y monitoreo"""
    ia_configured = bool(settings.OPENAI_API_KEY and 
                        (settings.OPENAI_API_KEY.startswith("sk-") or 
                         settings.OPENAI_API_KEY.startswith("gsk_") or
                         settings.OPENAI_API_KEY.startswith("gl-") or
                         len(settings.OPENAI_API_KEY) > 20))
    
    is_groq = settings.OPENAI_BASE_URL and "groq" in str(settings.OPENAI_BASE_URL).lower()
    is_openai = not is_groq and settings.OPENAI_API_KEY and settings.OPENAI_API_KEY.startswith("sk-")
    
    if is_groq:
        provider = "groq"
    elif is_openai:
        provider = "openai"
    else:
        provider = "unknown"
    
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "triage-ia-backend",
        "ia_configured": ia_configured,
        "ia_provider": provider if ia_configured else None,
        "ia_model": settings.OPENAI_MODEL if ia_configured else None
    }

@app.get("/test-ia")
async def test_ia_connection():
    """Endpoint para probar la conexión con OpenAI/Groq"""
    from app.services.ia_service import ia_service
    
    is_groq = settings.OPENAI_BASE_URL and "groq" in str(settings.OPENAI_BASE_URL).lower()
    provider = "Groq" if is_groq else "OpenAI"
    
    try:
        # Verificar si el cliente está inicializado
        if ia_service.client is None:
            return {
                "success": False,
                "error": f"Cliente {provider} no inicializado - API Key no configurada",
                "api_key_preview": settings.OPENAI_API_KEY[:15] + "..." if settings.OPENAI_API_KEY else None
            }
        
        # Intentar una llamada simple de prueba
        response = await ia_service.client.chat.completions.create(
            model=settings.OPENAI_MODEL,
            messages=[
                {"role": "system", "content": "Responde 'OK' si estas funcionando."},
                {"role": "user", "content": "Test"}
            ],
            max_tokens=5,
            timeout=10.0
        )
        
        return {
            "success": True,
            "message": f"Conexion con {provider} exitosa",
            "provider": provider,
            "model": settings.OPENAI_MODEL,
            "response": response.choices[0].message.content,
            "api_key_preview": settings.OPENAI_API_KEY[:15] + "..."
        }
        
    except Exception as e:
        error_msg = str(e)
        logger.error(f"Error en test de IA: {error_msg}")
        suggestion = "https://console.groq.com" if is_groq else "https://platform.openai.com"
        return {
            "success": False,
            "error": error_msg,
            "provider": provider,
            "api_key_preview": settings.OPENAI_API_KEY[:15] + "..." if settings.OPENAI_API_KEY else None,
            "suggestion": f"Verifique que la API Key sea valida en {suggestion}"
        }

@app.post("/trigger-critical-alert")
async def trigger_critical_alert(data: dict):
    """Dispara alerta crítica a n8n via webhook"""
    try:
        webhook_url = "http://n8n:5678/webhook-test/webhook/critical-alert"
        
        async with httpx.AsyncClient() as client:
            response = await client.post(webhook_url, json=data, timeout=10.0)
            response.raise_for_status()
        
        logger.info(f"Alerta crítica enviada a n8n: {data.get('nivel_urgencia_final', 'UNKNOWN')}")
        return {"status": "triggered", "message": "Alerta enviada a n8n"}
        
    except httpx.HTTPStatusError as e:
        logger.error(f"Error HTTP al enviar alerta a n8n: {e}")
        raise HTTPException(status_code=500, detail=f"Error al enviar alerta: {e}")
    except Exception as e:
        logger.error(f"Error al enviar alerta crítica: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")

# ============================================
# Manejadores de excepciones globales
# ============================================

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Manejador personalizado para errores HTTP"""
    if exc.status_code == status.HTTP_409_CONFLICT:
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "success": False,
                "error": "CONCURRENCY_ERROR",
                "message": exc.detail,
                "suggestion": "Por favor recargue los datos y reintente"
            }
        )
    return JSONResponse(
        status_code=exc.status_code,
        content={"success": False, "message": exc.detail}
    )

@app.exception_handler(SQLAlchemyError)
async def sqlalchemy_exception_handler(request: Request, exc: SQLAlchemyError):
    """Manejador para errores de base de datos"""
    logger.error(f"Error de base de datos: {str(exc)}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "success": False,
            "error": "DATABASE_ERROR",
            "message": "Error en la base de datos. Por favor intente más tarde."
        }
    )

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Manejador global para errores no controlados"""
    logger.error(f"Error no controlado: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "success": False,
            "error": "INTERNAL_ERROR",
            "message": "Error interno del servidor. Por favor intente más tarde."
        }
    )

# ============================================
# Eventos de ciclo de vida
# ============================================

@app.on_event("startup")
async def startup_event():
    """Inicialización al arrancar el servidor"""
    logger.info("=" * 50)
    logger.info("Iniciando FastAPI Backend - Sistema de Triaje IA")
    logger.info("=" * 50)
    
    # 1. Verificar conexión a PostgreSQL
    try:
        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
        logger.info("✅ Conexión a PostgreSQL establecida")
    except Exception as e:
        logger.error(f"❌ Error conectando a PostgreSQL: {str(e)}")
        logger.error("   El sistema no funcionará correctamente sin base de datos")
    
    # 2. Crear tablas si no existen
    try:
        from app.database import init_db
        await init_db()
        logger.info("✅ Tablas creadas/verificadas")
    except Exception as e:
        logger.error(f"❌ Error creando tablas: {str(e)}")
    
    # 3. Verificar configuración de IA (OpenAI o Groq)
    is_groq = settings.OPENAI_BASE_URL and "groq" in str(settings.OPENAI_BASE_URL).lower()
    provider = "Groq" if is_groq else "OpenAI"
    
    is_valid_key = bool(settings.OPENAI_API_KEY and len(settings.OPENAI_API_KEY) > 10)
    
    if is_valid_key:
        logger.info(f"✅ {provider} configurado (Modelo: {settings.OPENAI_MODEL})")
        logger.info(f"   Base URL: {settings.OPENAI_BASE_URL or 'https://api.openai.com/v1'}")
    else:
        logger.warning("⚠️  ADVERTENCIA: API Key de IA no configurada")
        logger.warning("   La funcionalidad de IA no estará disponible")
        logger.warning("   Configure en .env: OPENAI_API_KEY y OPENAI_BASE_URL (para Groq)")
    
    # 4. Información de CORS
    logger.info(f"🌐 CORS permitido para: {ALLOWED_ORIGINS}")
    
    # 5. Resumen final
    logger.info("=" * 50)
    logger.info("🚀 Servidor listo para recibir peticiones")
    logger.info("=" * 50)

@app.on_event("shutdown")
async def shutdown_event():
    """Limpieza al apagar el servidor"""
    logger.info("Cerrando conexiones...")
    await engine.dispose()
    logger.info("✅ Conexiones cerradas correctamente")

# ============================================
# Punto de entrada para desarrollo local
# ============================================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )