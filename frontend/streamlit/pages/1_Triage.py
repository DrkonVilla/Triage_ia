import streamlit as st
import pandas as pd
from datetime import datetime, date
from utils import *
from streamlit import session_state as ss
import sys
import os
import requests
import json

# Agregar parent al path para importar auth_persistence
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from components.auth_persistence import verify_and_restore_session

st.set_page_config(page_title="Nuevo Triaje", page_icon="📝", layout="wide")

# Intentar restaurar sesión si no está autenticado
API_BASE_URL = "http://localhost:8000"
if not st.session_state.get('authenticated'):
    if verify_and_restore_session(API_BASE_URL):
        st.rerun()

def trigger_critical_alert(triaje_data):
    """Dispara alerta crítica a n8n via FastAPI"""
    try:
        alert_data = {
            "nivel_urgencia_final": triaje_data.get('nivelUrgenciaFinal', 'UNKNOWN'),
            "paciente_nombre_completo": f"{triaje_data.get('pacienteNombres', '')} {triaje_data.get('pacienteApellidos', '')}".strip(),
            "motivo_consulta": triaje_data.get('motivoConsulta', ''),
            "id": triaje_data.get('id', 0),
            "timestamp": datetime.now().isoformat()
        }
        
        response = requests.post(f"{API_BASE_URL}/trigger-critical-alert", json=alert_data, timeout=10)
        response.raise_for_status()
        
        st.success("🚨 Alerta crítica enviada a médicos via Telegram")
        return True
        
    except requests.exceptions.RequestException as e:
        st.warning(f"⚠️ No se pudo enviar alerta crítica: {str(e)}")
        return False
    except Exception as e:
        st.error(f"❌ Error inesperado al enviar alerta: {str(e)}")
        return False

# Verificar autenticación y rol
if 'authenticated' not in st.session_state or st.session_state.get('user_role') != 'enfermera':
    st.error("Acceso no autorizado. Solo personal de enfermería puede acceder.")
    st.stop()

# Helper para renderizar HTML sin mostrar código fuente
def render_html(html_content: str):
    """Renderiza HTML usando st.html() si está disponible, o st.markdown como fallback"""
    html_clean = html_content.strip()
    if hasattr(st, 'html'):
        st.html(html_clean)
    else:
        st.markdown(html_clean, unsafe_allow_html=True)

# Header moderno
render_html("""<h1 style="font-size: 28px; font-weight: 700; color: #0D47A1; margin-bottom: 8px;">
    📝 Nuevo Registro de Triaje
</h1>
<p style="color: #616161; margin-bottom: 24px;">
    Complete el formulario paso a paso para registrar un nuevo paciente en el sistema de triaje
</p>""")

# Wizard Steps
def render_wizard_steps(current_step: int):
    steps = ["👤 Paciente", "🏥 Triaje", "🤖 IA", "✅ Confirmar"]
    step_classes = []
    for i, step in enumerate(steps):
        if i < current_step:
            step_classes.append("background: #43A047; color: white; border-color: #43A047;")  # completed
        elif i == current_step:
            step_classes.append("background: #1E88E5; color: white; border-color: #1E88E5;")  # active
        else:
            step_classes.append("background: white; color: #9E9E9E; border-color: #E0E0E0;")  # pending
    
    html_parts = ['<div style="display: flex; align-items: center; gap: 8px; margin-bottom: 32px; padding: 16px; background: #FAFAFA; border-radius: 16px;">']
    for i, (step, cls) in enumerate(zip(steps, step_classes)):
        html_parts.append(f'<div style="{cls} padding: 10px 16px; border-radius: 8px; font-size: 14px; font-weight: 500; border: 1px solid; white-space: nowrap;">{step}</div>')
        if i < len(steps) - 1:
            html_parts.append('<div style="flex: 1; height: 2px; background: #E0E0E0; max-width: 40px;"></div>')
    html_parts.append('</div>')
    render_html(''.join(html_parts))

# Determinar paso actual
current_step = 0
if st.session_state.get('paciente_seleccionado'):
    current_step = 1
if st.session_state.get('triaje_creado'):
    current_step = 2
if st.session_state.get('triaje_confirmado'):
    current_step = 3

render_wizard_steps(current_step)

# --- PASO 1: Búsqueda/Registro de Paciente ---
with st.container(border=True):
    render_html("""<div style="display: flex; align-items: center; gap: 12px; margin-bottom: 16px; padding-bottom: 12px; border-bottom: 1px solid #EEEEEE;">
    <div style="width: 32px; height: 32px; border-radius: 50%; background: #1E88E5; color: white; display: flex; align-items: center; justify-content: center; font-weight: 600; font-size: 14px;">1</div>
    <h3 style="font-size: 18px; font-weight: 600; color: #212121; margin: 0;">Identificación del Paciente</h3>
</div>""")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("**🔍 Buscar paciente existente**")
        search_term = st.text_input("DNI o Nombre:", placeholder="Ej: 12345678A o María García", label_visibility="collapsed")
        if st.button("🔍 Buscar Paciente", type="primary"):
            if search_term:
                paciente = buscar_paciente(search_term)
                if paciente:
                    st.session_state['paciente_seleccionado'] = paciente
                    st.success(f"✅ Paciente encontrado: {paciente['nombres']} {paciente['apellidos']}")
                    st.rerun()
                else:
                    st.warning("⚠️ No se encontró el paciente. Puede registrar uno nuevo.")
                    st.session_state['paciente_seleccionado'] = None
            else:
                st.warning("Ingrese un término de búsqueda")
    
    with col2:
        st.markdown("**➕ Nuevo paciente**")
        if st.button("🆕 Registrar Nuevo", use_container_width=True):
            st.session_state['show_registro_paciente'] = True
            st.rerun()

# Formulario de registro de nuevo paciente
if st.session_state.get('show_registro_paciente', False):
    with st.expander("Formulario de Registro de Paciente", expanded=True):
        col1, col2, col3 = st.columns(3)
        with col1:
            dni = st.text_input("DNI *", key="nuevo_dni")
            nombres = st.text_input("Nombres *", key="nuevo_nombres")
            apellidos = st.text_input("Apellidos *", key="nuevo_apellidos")
        with col2:
            fecha_nac = st.date_input("Fecha de Nacimiento *", key="nuevo_fecha")
            genero = st.selectbox("Género", ["M", "F", "Otros"], key="nuevo_genero")
            telefono = st.text_input("Teléfono", key="nuevo_telefono")
        with col3:
            email = st.text_input("Email", key="nuevo_email")
            direccion = st.text_area("Dirección", key="nuevo_direccion")
        
        if st.button("💾 Guardar Paciente"):
            if dni and nombres and apellidos and fecha_nac:
                nuevo_paciente = {
                    "dni": dni,
                    "nombres": nombres,
                    "apellidos": apellidos,
                    "fecha_nacimiento": fecha_nac.isoformat(),
                    "genero": genero,
                    "telefono": telefono if telefono else None,
                    "email": email if email else None,
                    "direccion": direccion if direccion else None,
                    "contactos_emergencia": []
                }
                paciente_creado = crear_paciente(nuevo_paciente)
                if paciente_creado:
                    st.session_state['paciente_seleccionado'] = paciente_creado
                    st.success(f"✅ Paciente registrado: {nombres} {apellidos}")
                    st.session_state['show_registro_paciente'] = False
                    st.rerun()
            else:
                st.error("Complete los campos obligatorios (*)")

# --- Mostrar paciente seleccionado ---
if st.session_state.get('paciente_seleccionado'):
    paciente = st.session_state['paciente_seleccionado']
    
    # Calcular edad (API puede retornar `edad` y/o `fecha_nacimiento` como string)
    edad = paciente.get('edad')
    if edad is None:
        from datetime import date
        fecha_nacimiento = paciente.get('fecha_nacimiento') or paciente.get('fechaNacimiento')
        if isinstance(fecha_nacimiento, str):
            try:
                fecha_nacimiento = date.fromisoformat(fecha_nacimiento)
            except ValueError:
                fecha_nacimiento = None

        if isinstance(fecha_nacimiento, date):
            hoy = date.today()
            edad = hoy.year - fecha_nacimiento.year - (
                (hoy.month, hoy.day) < (fecha_nacimiento.month, fecha_nacimiento.day)
            )
        else:
            edad = "N/D"
    
    st.info(f"**Paciente:** {paciente['nombres']} {paciente['apellidos']} | **DNI:** {paciente['dni']} | **Edad:** {edad} años")
    
    # Botón para consultar HCE
    if st.button("📋 Consultar Historial Clínico (HCE)"):
        with st.spinner("Consultando antecedentes..."):
            hce_data = obtener_antecedentes_hce(paciente['id'])
            if hce_data:
                st.session_state['hce_data'] = hce_data
                st.success("Antecedentes cargados")
            else:
                st.info("No se encontraron antecedentes registrados")
    
    # Mostrar HCE en expander
    if st.session_state.get('hce_data'):
        with st.expander("📋 Antecedentes Clínicos (HCE)"):
            hce = st.session_state['hce_data']
            if hce.get('entry'):
                for entry in hce['entry']:
                    resource = entry.get('resource', {})
                    resource_type = resource.get('resourceType')
                    
                    if resource_type == 'Condition':
                        # FHIR format: code.coding[0].display or code.text
                        code = resource.get('code', {})
                        name = code.get('text') or (code.get('coding', [{}])[0].get('display') if code.get('coding') else None) or 'Sin nombre'
                        category = resource.get('category', {}).get('text') or 'Sin categoría'
                        st.markdown(f"**{name}** ({category})")
                        
                        notes = resource.get('note', [])
                        if notes and len(notes) > 0:
                            note_text = notes[0].get('text', '')
                            if note_text:
                                st.caption(note_text)
                    
                    elif resource_type == 'Encounter':
                        period_start = resource.get('period', {}).get('start', 'Fecha desconocida')
                        reason_codes = resource.get('reasonCode', [])
                        reason = reason_codes[0].get('text') if reason_codes and len(reason_codes) > 0 else 'Sin motivo'
                        st.markdown(f"📅 {period_start}: {reason}")
            else:
                st.text("Sin antecedentes registrados")
    
    st.markdown("---")
    
    # --- PASO 2: Signos Vitales y Síntomas ---
    st.subheader("Paso 2: Signos Vitales y Síntomas")
    
    # Sección de síntomas FUERA del form para actualización dinámica
    col_sintomas, col_vitales = st.columns(2)
    
    sintomas_lista = []
    
    with col_sintomas:
        st.markdown("#### Motivo y Síntomas")
        motivo_consulta = st.text_area("Motivo de Consulta *", height=100, 
                                      placeholder="Ej: Dolor torácico opresivo de 2 horas de evolución...")
        
        st.markdown("**Síntomas:**")
        
        # Selector de síntomas comunes - FUERA del form para actualización dinámica
        sintomas_opciones = st.multiselect(
            "Seleccione síntomas",
            ["Dolor_toracico", "Disnea", "Fiebre", "Cefalea", "Dolor_abdominal", 
             "Nauseas", "Mareos", "Palpitaciones", "Tos", "Cianosis"]
        )
        
        # Campos de intensidad aparecen dinámicamente al seleccionar síntomas
        for sintoma in sintomas_opciones:
            col_a, col_b = st.columns([2, 1])
            with col_a:
                intensidad = st.selectbox(f"Intensidad - {sintoma}", ["Leve", "Moderado", "Grave"], key=f"int_{sintoma}")
            with col_b:
                desc = st.text_input(f"Descripción (opcional)", key=f"desc_{sintoma}", placeholder="Detalles...")
            sintomas_lista.append({
                "sintoma": sintoma,
                "intensidad": intensidad,
                "descripcion_libre": desc if desc else None
            })
        
        # Síntoma libre
        sintoma_libre = st.text_input("Otro síntoma (especificar)", key="sintoma_libre_input")
        if sintoma_libre:
            intensidad_libre = st.selectbox("Intensidad", ["Leve", "Moderado", "Grave"], key="int_libre")
            sintomas_lista.append({
                "sintoma": sintoma_libre,
                "intensidad": intensidad_libre,
                "descripcion_libre": None
            })
    
    with col_vitales:
        st.markdown("#### Signos Vitales")
        presion_sistolica = st.number_input("Presión Sistólica (mmHg)", min_value=50, max_value=250, value=120)
        presion_diastolica = st.number_input("Presión Diastólica (mmHg)", min_value=30, max_value=200, value=80)
        frecuencia_cardiaca = st.number_input("Frecuencia Cardíaca (lpm)", min_value=30, max_value=250, value=80)
        frecuencia_respiratoria = st.number_input("Frecuencia Respiratoria (rpm)", min_value=5, max_value=60, value=16)
        temperatura = st.number_input("Temperatura (°C)", min_value=30.0, max_value=45.0, value=36.5, step=0.1)
        saturacion_o2 = st.slider("Saturación O2 (%)", 0, 100, 97)
    
    # Validación
    if not motivo_consulta:
        st.warning("⚠️ El motivo de consulta es obligatorio")
    
    # Botón de envío
    submitted = st.button("🚀 Evaluar con IA y Registrar Triaje", use_container_width=True, type="primary")
    
    # Procesar envío
    if submitted:
        if not motivo_consulta:
            st.error("❌ Debe ingresar el motivo de consulta antes de evaluar")
        else:
            with st.spinner("🩺 Evaluando caso clínico con IA. Por favor espere..."):
                # Preparar datos para API
                triaje_data = {
                    "paciente_id": paciente['id'],
                    "motivo_consulta": motivo_consulta,
                    "signos_vitales": {
                        "presion_sistolica": presion_sistolica,
                        "presion_diastolica": presion_diastolica,
                        "frecuencia_cardiaca": frecuencia_cardiaca,
                        "frecuencia_respiratoria": frecuencia_respiratoria,
                        "temperatura": temperatura,
                        "saturacion_o2": saturacion_o2,
                        "nota_suplementaria": None
                    },
                    "sintomas": sintomas_lista
                }
                
                # Llamar a API
                resultado = crear_triaje(triaje_data)
                
                if resultado:
                    # Guardar en session_state para mostrar fuera del form
                    st.session_state['ultimo_triaje'] = resultado
                    st.session_state['triaje_creado'] = True
                    
                    # Verificar si es alerta crítica (RED o ORANGE) y enviar notificación
                    nivel_final = resultado.get('nivelUrgenciaFinal', '').upper()
                    if nivel_final in ['RED', 'ORANGE']:
                        st.warning("🚨 Detectado nivel de urgencia crítico. Enviando alerta a médicos...")
                        trigger_critical_alert(resultado)
                    
                    st.success("✅ Triaje registrado exitosamente")
                    st.rerun()
                else:
                    st.error("Error al registrar el triaje. Por favor intente nuevamente.")
    
    # --- SECCIÓN DE CONFIRMACIÓN (fuera del formulario) ---
    if st.session_state.get('triaje_creado') and st.session_state.get('ultimo_triaje'):
        resultado = st.session_state['ultimo_triaje']
        
        # DEBUG: Ver respuesta completa (desplegable)
        with st.expander("🔧 Debug: Ver respuesta del servidor", expanded=False):
            st.json(resultado)
        
        # Mostrar sugerencia de IA
        st.markdown("### 🤖 Sugerencia del Sistema de IA")
        
        # Extraer nivel de urgencia - usar camelCase (formato de respuesta Pydantic)
        nivel_ia = resultado.get('nivelUrgenciaAsignadoIa') if resultado else None
        nivel_final = resultado.get('nivelUrgenciaFinal') if resultado else None
        notas_medicas = resultado.get('notasMedicas', '') if resultado else ''
        
        # Si nivel_ia es None pero nivel_final tiene valor, usar nivel_final
        if not nivel_ia and nivel_final:
            nivel_ia = nivel_final
            st.info("ℹ️ Usando nivel confirmado como sugerencia de IA")
        
        # Verificar si hay error de API Key
        if nivel_ia == "ERROR_API_KEY" or (not nivel_ia and "ERROR IA" in (notas_medicas or '')):
            st.error("""
            ⚠️ **Servicio de IA no disponible**
            
            La API Key no está configurada correctamente.
            
            **Para activar la IA:**
            1. Obtén una API Key en https://console.groq.com (recomendado) o https://platform.openai.com
            2. Agrega al archivo `.env`:
               ```
               OPENAI_API_KEY=gsk-tu-api-key-aqui
               OPENAI_BASE_URL=https://api.groq.com/openai/v1
               ```
            3. Reinicia el backend
            
            **Mientras tanto:** Asigne manualmente el nivel de urgencia.
            """)
            color = "#6c757d"  # Gris para indicar sin IA
        elif not nivel_ia:
            st.warning("⚠️ La IA no pudo determinar un nivel de urgencia. Por favor asigne manualmente.")
            st.info(f"Debug: nivel_ia={nivel_ia}, nivel_final={nivel_final}, notas={notas_medicas[:50] if notas_medicas else 'None'}...")
            color = "#6c757d"
        else:
            color = get_color_for_urgency(nivel_ia)
        
        if nivel_ia and nivel_ia != "ERROR_API_KEY":
            render_html(f"""<div style="background-color: {color}20; padding: 20px; border-radius: 10px; border-left: 5px solid {color}">
                <h3>Nivel de Urgencia Sugerido: {get_urgency_label(nivel_ia)}</h3>
            </div>""")
            
            # Mostrar diagnósticos sugeridos
            st.subheader("Diagnósticos Posibles Sugeridos")
            st.info("**La IA sugiere:** Evaluar síndrome compatible con el cuadro clínico presentado")
            
            st.subheader("Recomendaciones Conductuales")
            st.success("• Priorizar evaluación por médico tratante\n• Monitorizar signos vitales\n• Según evolución, considerar estudios complementarios")
        else:
            st.info("Asigne el nivel de urgencia manualmente basado en su criterio clínico.")
        
        # Opción para confirmar o cambiar nivel
        st.markdown("---")
        st.subheader("Validación por Enfermería")
        
        col1, col2 = st.columns(2)
        with col1:
            # Manejar caso cuando IA falla (nivel_ia es None)
            urgencias = ["RED", "ORANGE", "YELLOW", "GREEN", "BLUE"]
            default_index = urgencias.index(nivel_ia) if nivel_ia in urgencias else 2  # Default YELLOW
            nivel_final = st.selectbox(
                "Confirmar o modificar el nivel de urgencia:",
                urgencias,
                index=default_index,
                key="nivel_final_select"  # key único
            )
        
        with col2:
            st.markdown("####")
            if st.button("✅ Confirmar y Enviar a Cola Médica", type="primary"):
                if confirmar_nivel_urgencia(resultado['id'], nivel_final):
                    st.success("✅ Nivel confirmado. El paciente ha sido añadido a la cola de atención médica.")
                    st.balloons()
                    # Limpiar sesión
                    st.session_state['paciente_seleccionado'] = None
                    st.session_state['hce_data'] = None
                    st.session_state['ultimo_triaje'] = None
                    st.session_state['triaje_creado'] = False
                    st.rerun()
                else:
                    st.error("Error al confirmar el nivel")
    
else:
    st.info("👆 Busque o registre un paciente para comenzar el triaje")