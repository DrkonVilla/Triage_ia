# 🚀 Guía de Deploy - Stack Gratuito (Supabase + Render + n8n Cloud)

## 📋 Resumen de Servicios

| Componente | Servicio | Costo | URLs de ejemplo |
|------------|----------|-------|-----------------|
| **Base de datos** | Supabase | Gratis | - |
| **Backend (FastAPI)** | Render | Gratis | `https://triage-fastapi.onrender.com` |
| **Frontend (Streamlit)** | Render | Gratis | `https://triage-streamlit.onrender.com` |
| **Automatización** | n8n Cloud | Gratis (100 exec/mes) | `https://[username].app.n8n.cloud` |
| **Total** | | **$0/mes** | |

---

## 1️⃣ Supabase - Base de Datos PostgreSQL

### Paso 1: Crear cuenta y proyecto
1. Ve a https://supabase.com
2. Regístrate con GitHub
3. Click "New Project"
4. Selecciona tu organización
5. Configura:
   - **Name**: `triage-db`
   - **Database Password**: Genera una segura (guárdala)
   - **Region**: Selecciona la más cercana a tu ubicación
   - **Plan**: Free Tier
6. Click "Create new project"

### Paso 2: Obtener connection string
1. En el dashboard de tu proyecto, ve a **Settings** → **Database**
2. Selecciona modo **URI** (no pooled, es más simple para empezar)
3. Copia el **Connection string**, se verá así:
   ```
   postgresql://postgres:[YOUR-PASSWORD]@db.xxxxxxxxxxxxxxxxxxxx.supabase.co:5432/postgres
   ```
4. Reemplaza `[YOUR-PASSWORD]` con la contraseña que pusiste

### Paso 3: Crear tablas (migrar desde local)

**Opción A: Usando SQL Editor en Supabase**
1. Ve a **SQL Editor** en el sidebar
2. New query → Copia el contenido de `database/init.sql`
3. Click **Run**

**Opción B: Migrar desde tu BD local**
```powershell
# En tu máquina local, hacer backup
docker compose exec postgres pg_dump -U triaje_user triaje_db > supabase_backup.sql

# Luego en Supabase SQL Editor, copia y pega el contenido de supabase_backup.sql
```

---

## 2️⃣ Render - FastAPI + Streamlit

### Paso 1: Subir código a GitHub
```powershell
git add .
git commit -m "Prepare for Supabase + Render deploy"
git push origin main
```

### Paso 2: Crear cuenta en Render
1. Ve a https://render.com
2. Regístrate con GitHub
3. Conecta tu repositorio

### Paso 3: Deploy FastAPI Backend
1. En Render Dashboard → **Blueprints**
2. Click **New Blueprint Instance**
3. Selecciona tu repositorio
4. Selecciona el archivo `render-supabase.yaml`
5. Click **Apply**

### Paso 4: Configurar variables secretas
Después de crear el blueprint, configura estas variables en cada servicio:

**Para `triage-fastapi`:**
- `DATABASE_URL` = Connection string de Supabase
- `OPENAI_API_KEY` = Tu API key de Groq
- `TELEGRAM_BOT_TOKEN` = Token del bot de Telegram
- `TELEGRAM_CHAT_ID` = Chat ID (ej: 6988461582)
- `N8N_WEBHOOK_URL` = URL de webhook de n8n Cloud (lo obtendremos en paso 3)

---

## 3️⃣ n8n Cloud - Automatización

### Paso 1: Crear cuenta
1. Ve a https://n8n.cloud
2. Regístrate
3. Elige plan **Starter** (gratis con 100 ejecuciones/mes)

### Paso 2: Configurar workflow
1. En n8n Cloud, crea un nuevo workflow
2. Agrega un nodo **Webhook**:
   - **Method**: POST
   - **Path**: `/critical-alert`
   - **Response**: "Using 'Respond to Webhook' Node"
3. Agrega un nodo **Code** (Formatear Mensaje):
   ```javascript
   const paciente = $input.first().json;
   
   const nombre = paciente.paciente_nombre_completo || paciente.pacienteNombreCompleto || 'Paciente';
   const nivel = paciente.nivel_urgencia_final || paciente.nivelUrgenciaFinal;
   const motivo = paciente.motivo_consulta || paciente.motivoConsulta || 'N/A';
   const id = paciente.id || paciente.Id;
   const timestamp = new Date().toLocaleString('es-CL');
   
   const mensaje = `🚨 *ALERTA DE TRIAJE* 🚨
   
   🏥 *Paciente:* ${nombre}
   ⚠️ *Nivel:* ${nivel === 'RED' ? '🔴 CRÍTICO' : '🟠 URGENTE'}
   📝 *Motivo:* ${motivo}
   🆔 *ID Triaje:* ${id}
   
   ⏰ *Timestamp:* ${timestamp}
   📍 *Unidad:* Emergencia`;
   
   return [{ 
     json: { 
       chat_id: '6988461582',  // Tu chat ID
       text: mensaje, 
       parse_mode: 'Markdown' 
     } 
   }];
   ```
4. Agrega un nodo **Telegram** (Send Message):
   - **Credentials**: Crea nueva con tu bot token
   - **Chat ID**: `6988461582`
   - **Text**: `{{ $json.text }}`
   - **Parse Mode**: Markdown

### Paso 3: Obtener webhook URL
1. Activa el workflow (toggle en ON)
2. En el nodo Webhook, copia la **Production URL**:
   ```
   https://[username].app.n8n.cloud/webhook/critical-alert
   ```
3. Esta URL es la que usarás en `N8N_WEBHOOK_URL` en Render

---

## 4️⃣ Configuración Final

### Paso 1: Actualizar N8N_WEBHOOK_URL en Render
1. Ve a Render Dashboard → `triage-fastapi` → Environment
2. Agrega/actualiza:
   ```
   N8N_WEBHOOK_URL=https://[username].app.n8n.cloud/webhook/critical-alert
   ```
3. Click **Save Changes**
4. El servicio se reiniciará automáticamente

### Paso 2: Actualizar Streamlit API_URL
Si usaste el blueprint, ya está configurado como:
```
API_BASE_URL=https://triage-fastapi.onrender.com
```

### Paso 3: Verificar conexión
```powershell
# Test FastAPI
curl https://triage-fastapi.onrender.com/health

# Test Streamlit
curl https://triage-streamlit.onrender.com/_stcore/health
```

---

## 🔗 URLs Finales

| Servicio | URL |
|----------|-----|
| **FastAPI API Docs** | `https://triage-fastapi.onrender.com/docs` |
| **Streamlit App** | `https://triage-streamlit.onrender.com` |
| **n8n Editor** | `https://[username].app.n8n.cloud` |
| **Supabase Dashboard** | `https://app.supabase.com/project/[project-ref]` |

---

## ⚠️ Limitaciones Free Tier

### Supabase Free
- 500MB de almacenamiento
- 50,000 queries/día
- 2GB transferencia/mes
- **Sleep después de 7 días** de inactividad (se despierta automáticamente)

### Render Free
- 512MB RAM por servicio
- **Sleep después de 15 min** de inactividad (tarda ~30s en despertar)
- 100GB ancho de banda/mes

### n8n Cloud Free
- 100 ejecuciones de workflow/mes
- Webhooks siempre activos
- Después de 100: $0.10 por ejecución adicional

---

## 🚀 Próximos pasos para escalar

Cuando necesites más recursos:

| Upgrade | De | A | Costo |
|---------|-----|-----|-------|
| Supabase | Free | Pro ($25/mes) | 8GB storage, ilimitado |
| Render | Free | Starter ($7/servicio) | No sleep, más RAM |
| n8n Cloud | Free | Pro ($20/mes) | Ejecuciones ilimitadas |

---

## 🆘 Troubleshooting

### "Database connection failed"
- Verifica que el connection string esté correcto
- Asegúrate de usar la contraseña correcta
- Intenta con "Connection Pooler" en lugar de "Direct Connection" en Supabase

### "Webhook 404 not found"
- Verifica que el workflow de n8n esté activado (toggle verde)
- Asegúrate de usar la **Production URL**, no la Test URL

### "Telegram bot not responding"
- Verifica que el bot tenga permisos en el chat
- Prueba enviar mensaje manualmente con curl

---

## ✅ Checklist Final

- [ ] Cuenta Supabase creada y BD configurada
- [ ] Tablas migradas a Supabase
- [ ] Repositorio en GitHub
- [ ] Cuenta Render con blueprint aplicado
- [ ] Variables de entorno configuradas en Render
- [ ] Cuenta n8n Cloud con workflow creado
- [ ] Webhook URL copiada a Render
- [ ] Telegram bot configurado y funcionando
- [ ] URLs accesibles públicamente
- [ ] Test de triaje crítico realizado

---

¿Listo para hacer el deploy? 🚀
