# Guía de Despliegue en Producción

## Requisitos
- Docker 20.10+
- 4 vCPU, 8GB RAM
- 50GB SSD

## Variables de Entorno Críticas
- `SECRET_KEY`: Generar con `openssl rand -hex 32`
- `OPENAI_API_KEY`: API key válida
- `POSTGRES_PASSWORD`: Contraseña segura

## Escalado Horizontal
```yaml
fastapi:
  deploy:
    replicas: 3
  environment:
    DATABASE_POOL_SIZE: 20