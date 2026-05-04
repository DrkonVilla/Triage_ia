FROM python:3.11-slim

WORKDIR /app

# Instalar dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código
COPY . .

# Crear directorio para assets
RUN mkdir -p assets

# Puerto por defecto (Railway sobreescribe con $PORT)
EXPOSE 8501

# Variables de entorno por defecto (se sobreescriben en Railway)
ENV API_BASE_URL=https://triage-fastapi-production.up.railway.app/api/v1
ENV PYTHONUNBUFFERED=1

# Comando para Railway (usa $PORT que Railway provee)
CMD ["sh", "-c", "streamlit run app.py --server.port=${PORT:-8501} --server.address=0.0.0.0 --server.headless=true --server.enableCORS=false --server.enableXsrfProtection=false"]