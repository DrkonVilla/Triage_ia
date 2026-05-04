# 🏥 Sistema de Triaje Clínico Asistido por IA

## 📋 Descripción General

Sistema completo de triaje clínico con soporte de inteligencia artificial, diseñado para personal de enfermería y médicos, con dashboards gerenciales y automatización de flujos de trabajo.

**Características Principales:**
- ✅ Evaluación asistida por IA (OpenAI GPT-4)
- ✅ Control de concurrencia con bloqueo optimista
- ✅ Auditoría forense completa
- ✅ Tablero Kanban para médicos
- ✅ Dashboards interactivos (Plotly + Recharts)
- ✅ Automatización con n8n (alertas, sincronización, reportes)
- ✅ Integración simulada con HCE (FHIR)
- ✅ Reportes PDF automatizados

## 🚀 Inicio Rápido

### Prerrequisitos

- Docker y Docker Compose (v2.0+)
- 8GB RAM mínimo
- API Key de OpenAI (para usar IA)

### Instalación y Despliegue

```bash
# 1. Clonar repositorio
git clone https://github.com/hospital/triage-ia.git
cd triage-ia

# 2. Configurar variables de entorno
cp .env.example .env
# Editar .env con tus credenciales (OpenAI API Key, etc.)

# 3. Levantar todo el ecosistema
docker-compose up -d

# 4. Verificar que todos los servicios estén corriendo
docker-compose ps

# 5. Acceder a las aplicaciones
# Streamlit (Enfermería/Médico): http://localhost:8501
# React Admin (Gerencia): http://localhost:5173
# FastAPI Docs: http://localhost:8000/docs
# n8n Workflows: http://localhost:5678 (admin/admin123)
# pgAdmin: http://localhost:5050 (admin@hospital.com/admin123)