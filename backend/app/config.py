from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = "postgresql+asyncpg://triaje_user:triaje_pass@localhost:5432/triaje_db"
    
    # JWT
    SECRET_KEY: str = "your-super-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 480
    
    # OpenAI / Groq Configuration
    OPENAI_API_KEY: str = ""  # También funciona con Groq API Key
    OPENAI_MODEL: str = "gpt-4-turbo-preview"  # O modelos Groq: llama-3.3-70b-versatile, llama-3.1-8b-instant
    OPENAI_BASE_URL: Optional[str] = None  # Para Groq: https://api.groq.com/openai/v1
    
    # n8n Webhooks
    N8N_WEBHOOK_CRITICAL_ALERT: str = "http://localhost:5678/webhook/critical-alert"
    
    # HCE Mock
    MOCK_HCE_URL: str = "http://localhost:8080/api/fhir"
    
    class Config:
        env_file = "../.env"  # .env está en la raíz del proyecto
        env_file_encoding = "utf-8"
        case_sensitive = False
        extra = "ignore"

settings = Settings()