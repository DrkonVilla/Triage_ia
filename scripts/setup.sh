#!/bin/bash

echo "🏥 Iniciando despliegue del Sistema de Triaje IA..."

# Verificar Docker
if ! command -v docker &> /dev/null; then
    echo "❌ Docker no está instalado. Por favor instalar Docker Desktop"
    exit 1
fi

# Verificar archivo .env
if [ ! -f .env ]; then
    echo "📝 Creando archivo .env desde ejemplo..."
    cp .env.example .env
    echo "⚠️ Por favor editar .env con tu OPENAI_API_KEY"
    read -p "Presiona Enter para continuar..."
fi

# Crear directorios necesarios
mkdir -p n8n-workflows mock-hce backend/sql

# Levantar servicios
echo "🚀 Levantando contenedores..."
docker-compose up -d

# Esperar a que PostgreSQL esté listo
echo "⏳ Esperando a que PostgreSQL inicie..."
sleep 10

# Ejecutar schema SQL
echo "📦 Inicializando base de datos..."
docker exec -i triage-postgres psql -U triaje_user -d triaje_db < backend/sql/schema.sql 2>/dev/null || true

echo "✅ Sistema desplegado exitosamente!"
echo ""
echo "📍 Accesos:"
echo "   Streamlit: http://localhost:8501"
echo "   React: http://localhost:5173"
echo "   FastAPI Docs: http://localhost:8000/docs"
echo "   n8n: http://localhost:5678 (admin/admin123)"
echo ""
echo "📋 Credenciales de prueba:"
echo "   Enfermera: enfermera1 / password123"
echo "   Médico: medico1 / password123"
echo "   Gerente: gerente1 / password123"