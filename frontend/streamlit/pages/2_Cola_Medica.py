import streamlit as st
import requests
import pandas as pd
from datetime import datetime
from utils import *
import sys
import os

# Agregar parent al path para importar auth_persistence
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from components.auth_persistence import verify_and_restore_session

st.set_page_config(page_title="Cola de Atención Médica", page_icon="🩺", layout="wide")

# Intentar restaurar sesión si no está autenticado
# API_BASE_URL se importa desde utils.py (usa variable de entorno)
if not st.session_state.get('authenticated'):
    if verify_and_restore_session(API_BASE_URL):
        st.rerun()

# Verificar autenticación y rol
if 'authenticated' not in st.session_state or st.session_state.get('user_role') != 'medico':
    st.error("Acceso no autorizado. Solo personal médico puede acceder.")
    st.stop()

# Header moderno
st.markdown("""
<h1 style="font-size: 28px; font-weight: 700; color: #0D47A1; margin-bottom: 8px;">
    🩺 Cola de Atención Médica
</h1>
<p style="color: #616161; margin-bottom: 24px;">
    Gestión de pacientes por nivel de urgencia - Vista Kanban
</p>
""", unsafe_allow_html=True)

# Auto-refresh cada 30 segundos
auto_refresh = st.checkbox("Auto-refrescar cada 30 segundos", value=True)
if auto_refresh:
    st.empty()
    st.caption("⏳ Actualizando automáticamente...")

# Función para cargar cola
def load_cola():
    headers = get_auth_headers()
    try:
        response = requests.get(f"{API_BASE_URL}/cola-medica/", headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Error cargando cola: {response.text}")
            return []
    except Exception as e:
        st.error(f"Error de conexión: {str(e)}")
        return []

# Estado de sesión para control
if 'triaje_en_edicion' not in st.session_state:
    st.session_state['triaje_en_edicion'] = None
if 'justificacion_modal' not in st.session_state:
    st.session_state['justificacion_modal'] = {}

# Cargar datos
cola_data = load_cola()

# Si auto-refresh, usar JavaScript para recargar sin bloquear UI
if auto_refresh:
    st.caption("🔄 Auto-refresh activado (30s)")
    # Usar JavaScript para recargar la página cada 30 segundos
    st.components.v1.html("""
    <script>
    // Auto-refresh cada 30 segundos
    setTimeout(function() {
        window.location.reload();
    }, 30000);
    
    // Mostrar cuenta regresiva
    let segundos = 30;
    const countdownEl = document.getElementById('countdown');
    if (countdownEl) {
        const interval = setInterval(function() {
            segundos--;
            countdownEl.textContent = '🔄 Recargando en ' + segundos + 's...';
            if (segundos <= 0) clearInterval(interval);
        }, 1000);
    }
    </script>
    <div id="countdown" style="color: #666; font-size: 12px; margin-top: 5px;">🔄 Recargando en 30s...</div>
    """, height=40)

if not cola_data:
    st.info("No hay pacientes en la cola de atención en este momento")
    st.stop()

# Orden de prioridad para triage
URGENCY_ORDER = {"RED": 1, "ORANGE": 2, "YELLOW": 3, "GREEN": 4, "BLUE": 5}

def get_urgency_priority(p):
    """Retorna prioridad numérica del paciente para ordenamiento"""
    nivel = (p.get('nivel_urgencia_final') or p.get('nivelUrgenciaFinal') or 
             p.get('nivel_urgencia_asignado_ia') or p.get('nivelUrgenciaAsignadoIa') or 'BLUE')
    return URGENCY_ORDER.get(nivel, 5)

def get_fecha_hora(p):
    """Retorna fecha_hora para ordenamiento FIFO"""
    fh = p.get('fecha_hora') or p.get('fechaHora') or p.get('created_at') or p.get('createdAt') or ''
    return fh

# Organizar por estado logístico y ordenar por prioridad + FIFO
estados = ["En Espera", "Llamado", "En Atencion", "Atendido"]
pacientes_por_estado = {estado: [] for estado in estados}

for paciente in cola_data:
    # Manejar camelCase del backend (alias_generator)
    estado = paciente.get('estado_logistico') or paciente.get('estadoLogistico') or 'En Espera'
    pacientes_por_estado[estado].append(paciente)

# Ordenar cada columna: prioridad ASC + fecha_hora ASC
for estado in estados:
    pacientes_por_estado[estado].sort(key=lambda p: (get_urgency_priority(p), get_fecha_hora(p)))

# Mostrar Kanban
col1, col2, col3, col4 = st.columns(4)

with col1:
    espera_count = len(pacientes_por_estado["En Espera"])
    st.markdown(f"""
    <div style="background: #FAFAFA; border-radius: 12px; padding: 16px; height: 100%;">
        <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 16px; padding-bottom: 12px; border-bottom: 2px solid #E0E0E0;">
            <span style="font-size: 20px;">⏳</span>
            <span style="font-size: 16px; font-weight: 600; color: #424242;">En Espera</span>
            <span style="background: #E0E0E0; color: #616161; padding: 2px 8px; border-radius: 12px; font-size: 12px; font-weight: 500;">{espera_count}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    for p in pacientes_por_estado["En Espera"]:
        # Manejar camelCase o snake_case del backend
        nivel = p.get('nivel_urgencia_final') or p.get('nivelUrgenciaFinal') or p.get('nivel_urgencia_asignado_ia') or p.get('nivelUrgenciaAsignadoIa') or 'GREEN'
        color = get_color_for_urgency(nivel)
        nombre_completo = f"{p.get('paciente_nombre_completo') or p.get('pacienteNombreCompleto', 'N/A')}"
        edad = p.get('paciente_edad', '?')
        
        with st.container():
            st.markdown(f"""
            <div style="background-color: white; border-left: 5px solid {color}; padding: 10px; margin-bottom: 10px; border-radius: 5px; box-shadow: 0 1px 3px rgba(0,0,0,0.1)">
                <strong>{nombre_completo}</strong> ({edad} años)<br>
                <span style="color: {color}; font-weight: bold">{get_urgency_label(nivel)}</span><br>
                <small>📝 {(p.get('motivo_consulta') or p.get('motivoConsulta', 'N/A'))[:50]}...</small><br>
                <small>🕐 {(p.get('fecha_hora') or p.get('fechaHora', ''))[:16]}</small>
            </div>
            """, unsafe_allow_html=True)
            
            col_accion1, col_accion2 = st.columns(2)
            with col_accion1:
                pid = p.get('id') or p.get('Id')
                pversion = p.get('version') or p.get('Version') or 1
                if st.button("📞 Llamar", key=f"llamar_{pid}"):
                    success, msg = cambiar_estado_triaje(pid, "Llamado", version=pversion)
                    if success:
                        st.success(msg)
                        st.rerun()
                    else:
                        st.error(msg)
            with col_accion2:
                pid = p.get('id') or p.get('Id')
                if st.button("📋 Ver", key=f"ver_{pid}"):
                    st.session_state['triaje_en_edicion'] = pid
                    st.session_state[f'detalle_{pid}'] = p
            st.markdown("---")

with col2:
    llamado_count = len(pacientes_por_estado["Llamado"])
    st.markdown(f"""
    <div style="background: #FFF8E1; border-radius: 12px; padding: 16px; height: 100%;">
        <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 16px; padding-bottom: 12px; border-bottom: 2px solid #FFD54F;">
            <span style="font-size: 20px;">📞</span>
            <span style="font-size: 16px; font-weight: 600; color: #424242;">Llamado</span>
            <span style="background: #FFD54F; color: #424242; padding: 2px 8px; border-radius: 12px; font-size: 12px; font-weight: 500;">{llamado_count}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    for p in pacientes_por_estado["Llamado"]:
        nivel = p.get('nivel_urgencia_final') or p.get('nivelUrgenciaFinal') or p.get('nivel_urgencia_asignado_ia') or p.get('nivelUrgenciaAsignadoIa') or 'GREEN'
        color = get_color_for_urgency(nivel)
        nombre_completo = f"{p.get('paciente_nombre_completo') or p.get('pacienteNombreCompleto', 'N/A')}"
        
        with st.container():
            st.markdown(f"""
            <div style="background-color: #FFF8E1; border-left: 5px solid {color}; padding: 10px; margin-bottom: 10px; border-radius: 5px">
                <strong>{nombre_completo}</strong><br>
                <span style="color: {color}">{get_urgency_label(nivel)}</span><br>
                <small>⏰ Llamado</small>
            </div>
            """, unsafe_allow_html=True)
            
            pid = p.get('id') or p.get('Id')
            pversion = p.get('version') or p.get('Version') or 1
            col_a, col_b = st.columns(2)
            with col_a:
                if st.button("🩺 Atender", key=f"atender_{pid}"):
                    success, msg = cambiar_estado_triaje(pid, "En Atencion", version=pversion)
                    if success:
                        st.success(msg)
                        st.rerun()
                    else:
                        st.error(msg)
            with col_b:
                if st.button("↩️ Devolver", key=f"devolver_{pid}"):
                    st.session_state['justificacion_modal'][pid] = True
                    st.session_state['triaje_devolver'] = p
            st.markdown("---")

with col3:
    atencion_count = len(pacientes_por_estado["En Atencion"])
    st.markdown(f"""
    <div style="background: #E8F5E9; border-radius: 12px; padding: 16px; height: 100%;">
        <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 16px; padding-bottom: 12px; border-bottom: 2px solid #81C784;">
            <span style="font-size: 20px;">🩺</span>
            <span style="font-size: 16px; font-weight: 600; color: #424242;">En Atención</span>
            <span style="background: #81C784; color: white; padding: 2px 8px; border-radius: 12px; font-size: 12px; font-weight: 500;">{atencion_count}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    for p in pacientes_por_estado["En Atencion"]:
        nivel = p.get('nivel_urgencia_final') or p.get('nivelUrgenciaFinal') or p.get('nivel_urgencia_asignado_ia') or p.get('nivelUrgenciaAsignadoIa') or 'GREEN'
        color = get_color_for_urgency(nivel)
        nombre_completo = f"{p.get('paciente_nombre_completo') or p.get('pacienteNombreCompleto', 'N/A')}"
        
        with st.container():
            st.markdown(f"""
            <div style="background-color: #E8F5E9; border-left: 5px solid {color}; padding: 10px; margin-bottom: 10px; border-radius: 5px">
                <strong>{nombre_completo}</strong><br>
                <span style="color: {color}">{get_urgency_label(nivel)}</span>
            </div>
            """, unsafe_allow_html=True)
            
            pid = p.get('id') or p.get('Id')
            pversion = p.get('version') or p.get('Version') or 1
            col_nota, col_fin = st.columns(2)
            with col_nota:
                if st.button("✏️ Notas", key=f"editar_{pid}"):
                    st.session_state['triaje_en_edicion'] = pid
                    st.session_state[f'detalle_{pid}'] = p
            with col_fin:
                if st.button("✅ Finalizar", key=f"finrap_{pid}", type="primary"):
                    # Verificar si ya tiene diagnóstico
                    diag = p.get('diagnostico_final') or p.get('diagnosticoFinal') or p.get('notas_medicas') or p.get('notasMedicas', '')
                    if not diag or len(str(diag)) < 3:
                        st.error("⚠️ Debe registrar notas/diagnóstico antes de finalizar")
                        st.session_state['triaje_en_edicion'] = pid
                        st.session_state[f'detalle_{pid}'] = p
                    else:
                        success, msg = cambiar_estado_triaje(pid, "Atendido", version=pversion)
                        if success:
                            st.success("✅ Atención finalizada. Paciente egresado.")
                            st.rerun()
                        else:
                            st.error(msg)
            st.markdown("---")

with col4:
    atendidos_count = len(pacientes_por_estado["Atendido"])
    st.markdown(f"""
    <div style="background: #E3F2FD; border-radius: 12px; padding: 16px; height: 100%;">
        <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 16px; padding-bottom: 12px; border-bottom: 2px solid #64B5F6;">
            <span style="font-size: 20px;">✅</span>
            <span style="font-size: 16px; font-weight: 600; color: #424242;">Atendidos</span>
            <span style="background: #64B5F6; color: white; padding: 2px 8px; border-radius: 12px; font-size: 12px; font-weight: 500;">{atendidos_count}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    for p in pacientes_por_estado["Atendido"][:5]:  # Solo últimos 5
        nombre = p.get('paciente_nombre_completo') or p.get('pacienteNombreCompleto', 'N/A')
        fecha = p.get('fecha_hora') or p.get('fechaHora', '')
        tiempo_seg = p.get('tiempo_atencion_segundos') or p.get('tiempoAtencionSegundos')
        tiempo_str = ""
        if tiempo_seg:
            minutos = int(tiempo_seg // 60)
            segundos = int(tiempo_seg % 60)
            tiempo_str = f" - ⏱️ {minutos}m {segundos}s"
        st.markdown(f"- **{nombre}** ({fecha[:10]}){tiempo_str}")

# --- Modales para justificación (Devolver) ---
if st.session_state.get('triaje_devolver'):
    p = st.session_state['triaje_devolver']
    pid = p.get('id') or p.get('Id')
    pversion = p.get('version') or p.get('Version') or 1
    pnombre = p.get('paciente_nombre_completo') or p.get('pacienteNombreCompleto', 'N/A')
    if st.session_state['justificacion_modal'].get(pid, False):
        with st.expander(f"⚠️ Justificación para devolver a {pnombre}", expanded=True):
            justificacion = st.text_area("Motivo de devolución a triaje:", 
                                        placeholder="Ej: El paciente requiere reevaluación por nuevos síntomas...",
                                        key=f"just_{pid}")
            col_ok, col_cancel = st.columns(2)
            with col_ok:
                if st.button("✅ Confirmar Devolución", key=f"confirm_{pid}"):
                    if justificacion and len(justificacion) >= 10:
                        success, msg = cambiar_estado_triaje(pid, "En Espera", justificacion, pversion)
                        if success:
                            st.success("Paciente devuelto a triaje")
                            st.session_state['justificacion_modal'][pid] = False
                            st.session_state['triaje_devolver'] = None
                            st.rerun()
                        else:
                            st.error(msg)
                    else:
                        st.error("Debe proporcionar una justificación de al menos 10 caracteres")
            with col_cancel:
                if st.button("❌ Cancelar"):
                    st.session_state['justificacion_modal'][pid] = False
                    st.session_state['triaje_devolver'] = None
                    st.rerun()

def check_vital_sign_alerts(sv):
    alerts = []
    try:
        ps = int(sv.get('presion_sistolica') or sv.get('presionSistolica', 120))
        pd = int(sv.get('presion_diastolica') or sv.get('presionDiastolica', 80))
        if ps > 140 or pd > 90: alerts.append("⚠️ HTA")
        if ps < 90 or pd < 60: alerts.append("⚠️ Hipotensión")
        fc = int(sv.get('frecuencia_cardiaca') or sv.get('frecuenciaCardiaca', 80))
        if fc > 100: alerts.append("⚠️ Taquicardia")
        if fc < 60: alerts.append("⚠️ Bradicardia")
        fr = int(sv.get('frecuencia_respiratoria') or sv.get('frecuenciaRespiratoria', 16))
        if fr > 20: alerts.append("⚠️ Taquipnea")
        if fr < 12: alerts.append("⚠️ Bradipnea")
        temp = float(sv.get('temperatura') or sv.get('temperatura', 36.5))
        if temp > 38: alerts.append("⚠️ Fiebre")
        if temp < 36: alerts.append("⚠️ Hipotermia")
        spo2 = int(sv.get('saturacion_o2') or sv.get('saturacionO2', 97))
        if spo2 < 92: alerts.append("⚠️ Hipoxia")
    except: pass
    return alerts

# --- Detalle del Paciente (Expander/Dialog) ---
if st.session_state.get('triaje_en_edicion'):
    triaje_id = st.session_state['triaje_en_edicion']
    p = st.session_state.get(f'detalle_{triaje_id}')
    
    if p:
        pnombre_detalle = p.get('paciente_nombre_completo') or p.get('pacienteNombreCompleto', 'Paciente')
        with st.expander(f"📋 Detalle Clínico - {pnombre_detalle}", expanded=True):
            # Signos Vitales con alertas
            st.markdown("#### 🩺 Signos Vitales")
            sv = p.get('signos_vitales') or p.get('signosVitales') or {}
            alertas_sv = check_vital_sign_alerts(sv)
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("PA", f"{sv.get('presion_sistolica') or sv.get('presionSistolica', '?')}/{sv.get('presion_diastolica') or sv.get('presionDiastolica', '?')} mmHg")
                st.metric("FC", f"{sv.get('frecuencia_cardiaca') or sv.get('frecuenciaCardiaca', '?')} lpm")
            with col2:
                st.metric("FR", f"{sv.get('frecuencia_respiratoria') or sv.get('frecuenciaRespiratoria', '?')} rpm")
                st.metric("Temp", f"{sv.get('temperatura') or sv.get('temperatura', '?')} °C")
            with col3:
                st.metric("SpO2", f"{sv.get('saturacion_o2') or sv.get('saturacionO2') or sv.get('saturacionO2', '?')} %")
            
            if alertas_sv:
                st.warning("  ".join(alertas_sv))
            
            st.markdown("#### 📝 Motivo de Consulta")
            st.info(p.get('motivo_consulta') or p.get('motivoConsulta', 'N/A'))
            
            # Evaluación IA
            st.markdown("#### 🤖 Evaluación IA")
            nivel_ia = p.get('nivel_urgencia_asignado_ia') or p.get('nivelUrgenciaAsignadoIa')
            notas_ia = p.get('notas_medicas_ia') or p.get('notasMedicasIa') or p.get('notas_medicas') or p.get('notasMedicas', '')
            if nivel_ia:
                color_ia = get_color_for_urgency(nivel_ia)
                st.markdown(f"""
                <div style="padding: 12px; background-color: {color_ia}15; border-left: 4px solid {color_ia}; border-radius: 6px; margin-bottom: 12px;">
                    <strong>Nivel sugerido:</strong> {get_urgency_label(nivel_ia)}<br>
                    <small>{notas_ia[:200] if notas_ia else 'Sin recomendaciones adicionales'}</small>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.caption("Sin evaluación IA disponible")
            
            # Antecedentes HCE
            st.markdown("#### 📋 Antecedentes HCE")
            paciente_id = p.get('paciente_id') or p.get('pacienteId')
            if paciente_id:
                hce = obtener_antecedentes_hce(paciente_id)
                if hce and hce.get('entry'):
                    for entry in hce['entry'][:3]:
                        resource = entry.get('resource', {})
                        resource_type = resource.get('resourceType')
                        if resource_type == 'Condition':
                            code = resource.get('code', {})
                            name = code.get('text') or (code.get('coding', [{}])[0].get('display') if code.get('coding') else None) or 'Sin nombre'
                            st.markdown(f"• **{name}**")
                        elif resource_type == 'AllergyIntolerance':
                            code = resource.get('code', {})
                            name = code.get('text') or 'Alergia'
                            st.markdown(f"• 🚨 **Alergia:** {name}")
                else:
                    st.caption("No se encontraron antecedentes registrados")
            else:
                st.caption("ID de paciente no disponible")
            
            st.markdown("---")
            
            st.markdown("#### 📝 Notas Médicas")
            notas_actuales = p.get('notas_medicas') or p.get('notasMedicas', '')
            nuevas_notas = st.text_area("Agregar notas clínicas:", value=notas_actuales if notas_actuales else "", height=150, key=f"notas_{triaje_id}")
            
            st.markdown("#### 🩺 Diagnóstico Final Médico *(Obligatorio para finalizar)*")
            diagnostico_final = st.text_input("Diagnóstico Final:", 
                                             value=p.get('diagnostico_final') or p.get('diagnosticoFinal') or '',
                                             placeholder="Ej: Infarto agudo de miocardio, Neumonía adquirida...",
                                             key=f"diag_{triaje_id}")
            
            if not diagnostico_final:
                st.error("⚠️ El diagnóstico final es obligatorio para finalizar la atención")
            
            # Obtener estado actual del paciente para condicionar botón Finalizar
            estado_paciente = p.get('estado_logistico') or p.get('estadoLogistico', '')
            puede_finalizar = estado_paciente == "En Atencion"
            
            if puede_finalizar:
                col_guardar, col_finalizar = st.columns(2)
            else:
                col_guardar = st.container()
                
            with col_guardar:
                if st.button("💾 Guardar Notas", key=f"guardar_{triaje_id}"):
                    headers = get_auth_headers()
                    try:
                        response = requests.put(
                            f"{API_BASE_URL}/cola-medica/{triaje_id}/notas-medicas",
                            params={"notas": nuevas_notas, "diagnostico_final": diagnostico_final},
                            headers=headers
                        )
                        if response.status_code == 200:
                            st.success("✅ Notas y diagnóstico guardados")
                            st.rerun()
                        else:
                            st.error("Error guardando notas")
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
            
            if puede_finalizar:
                with col_finalizar:
                    if st.button("✅ Finalizar Atención", type="primary", key=f"fin_{triaje_id}"):
                        if not diagnostico_final:
                            st.error("⚠️ El diagnóstico final es obligatorio para finalizar la atención")
                        else:
                            headers = get_auth_headers()
                            try:
                                # PASO 1: Guardar diagnóstico (esto incrementa la versión en el backend)
                                response = requests.put(
                                    f"{API_BASE_URL}/cola-medica/{triaje_id}/notas-medicas",
                                    params={"notas": nuevas_notas, "diagnostico_final": diagnostico_final},
                                    headers=headers
                                )
                                
                                if response.status_code == 200:
                                    # PASO 2: Recargar paciente para obtener la NUEVA versión 
                                    # (guardar notas incrementó la versión)
                                    refresh_resp = requests.get(
                                        f"{API_BASE_URL}/triaje/{triaje_id}",
                                        headers=headers,
                                        timeout=10
                                    )
                                    
                                    if refresh_resp.status_code == 200:
                                        paciente_actual = refresh_resp.json()
                                        version_actual = paciente_actual.get('version') or paciente_actual.get('Version') or 1
                                    else:
                                        version_actual = p.get('version') or p.get('Version') or 1
                                    
                                    # PASO 3: Cambiar estado a Atendido con la versión actualizada
                                    success, msg = cambiar_estado_triaje(triaje_id, "Atendido", version=version_actual)
                                    if success:
                                        st.success("✅ Atención finalizada. Paciente egresado.")
                                        st.session_state['triaje_en_edicion'] = None
                                        st.rerun()
                                    else:
                                        st.error(msg)
                                        if "CONFLICTO" in msg:
                                            st.info("💡 El registro fue modificado por otro usuario. Recargue la página para obtener los datos actualizados.")
                                            if st.button("🔄 Recargar página"):
                                                st.rerun()
                                else:
                                    st.error("Error guardando diagnóstico")
                            except Exception as e:
                                st.error(f"Error: {str(e)}")