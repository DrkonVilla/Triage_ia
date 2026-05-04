from fastapi import FastAPI, HTTPException, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
import logging
from datetime import datetime
import httpx

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

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especificar orígenes
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(auth.router)
app.include_router(pacientes.router)
app.include_router(triaje.router)
app.include_router(cola_medica.router)
app.include_router(hce.router)
app.include_router(auditoria.router)
app.include_router(reportes.router)

# Health check
@app.get("/health")
async def health_check():
    ia_configured = bool(settings.OPENAI_API_KEY and 
                        (settings.OPENAI_API_KEY.startswith("sk-") or settings.OPENAI_API_KEY.startswith("gsk_")))
    is_groq = settings.OPENAI_BASE_URL and "groq" in settings.OPENAI_BASE_URL
    provider = "groq" if is_groq else "openai"
    
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
    
    is_groq = settings.OPENAI_BASE_URL and "groq" in settings.OPENAI_BASE_URL
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

# Manejador global de excepciones para conflictos de concurrencia
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
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

@app.on_event("startup")
async def startup_event():
    logger.info("Iniciando FastAPI Backend...")
    # Verificar conexión a DB
    try:
        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
        logger.info("Conexión a PostgreSQL establecida")
        
        # Crear tablas si no existen
        from app.database import init_db
        await init_db()
        logger.info("✅ Tablas creadas/verificadas")
        
    except Exception as e:
        logger.error(f"Error conectando a PostgreSQL: {str(e)}")
    
    # Verificar configuración de IA (OpenAI o Groq)
    is_groq = settings.OPENAI_BASE_URL and "groq" in settings.OPENAI_BASE_URL
    provider = "Groq" if is_groq else "OpenAI"
    
    is_valid_key = settings.OPENAI_API_KEY and (
        settings.OPENAI_API_KEY.startswith("sk-") or settings.OPENAI_API_KEY.startswith("gsk_")
    )
    
    if is_valid_key:
        logger.info(f"✅ {provider} configurado (Modelo: {settings.OPENAI_MODEL})")
    else:
        logger.warning("⚠️  ADVERTENCIA: API Key de IA no configurada")

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
        logger.warning("   La funcionalidad de IA no estara disponible")
        logger.warning("   Configure en .env: OPENAI_API_KEY + OPENAI_BASE_URL (para Groq)")

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Cerrando conexiones...")
    await engine.dispose()