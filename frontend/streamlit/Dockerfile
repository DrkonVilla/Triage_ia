FROM python:3.11-slim

WORKDIR /app

# Instalar dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código
COPY . .

# Crear directorio para assets
RUN mkdir -p assets

EXPOSE 8501

CMD ["sh", "-c", "streamlit run app.py --server.port $PORT --server.address 0.0.0.0"]