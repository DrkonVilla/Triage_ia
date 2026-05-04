import streamlit as st
import yaml
from yaml.loader import SafeLoader
import requests
from datetime import datetime
import pandas as pd
import os

# Importar utilidades de autenticación
from utils import get_auth_headers
from components.auth_persistence import (
    verify_and_restore_session, 
    persist_login, 
    logout_and_clear,
    sync_token_from_storage
)

# Configuración de página
st.set_page_config(
    page_title="Sistema de Triaje Clínico Asistido por IA",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
with open('assets/styles.css', encoding='utf-8') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

_secrets_paths = [
    os.path.join(os.path.expanduser("~"), ".streamlit", "secrets.toml"),
    os.path.join(os.path.dirname(__file__), ".streamlit", "secrets.toml"),
]
if any(os.path.exists(p) for p in _secrets_paths):
    API_BASE_URL = st.secrets.get("API_BASE_URL", "http://localhost:8000")
else:
    API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")


def _get_query_params() -> dict:
    if hasattr(st, "query_params"):
        return dict(st.query_params)
    return st.experimental_get_query_params()


def _set_query_params(**kwargs):
    if hasattr(st, "query_params"):
        st.query_params.clear()
        for k, v in kwargs.items():
            if v is None or v == "":
                continue
            st.query_params[k] = v
        return
    st.experimental_set_query_params(**{k: v for k, v in kwargs.items() if v is not None and v != ""})


def _nav_link(page_path: str, label: str, icon: str):
    if hasattr(st, "page_link"):
        st.page_link(page_path, label=label, icon=icon)
        return

    if page_path == "app.py":
        if st.button(label):
            st.rerun()
    else:
        if st.button(label):
            st.switch_page(page_path)

# Inicializar estado de autenticación
if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False

# Intentar restaurar sesión silenciosamente si no está autenticado
if not st.session_state.get('authenticated'):
    if verify_and_restore_session(API_BASE_URL):
        st.rerun()

if not st.session_state.get('authenticated'):
    # Contenedor de login centrado
    st.markdown("""
    <style>
    .login-wrapper {
        min-height: 100vh;
        display: flex;
        align-items: center;
        justify-content: center;
        background: linear-gradient(135deg, #E3F2FD 0%, #E0F7FA 100%);
        margin: -6rem -4rem -10rem -4rem;
        padding: 2rem;
    }
    .login-card-container {
        max-width: 440px;
        width: 100%;
    }
    </style>
    <div class="login-wrapper">
        <div class="login-card-container">
    """, unsafe_allow_html=True)
    
    # Card de login
    st.markdown("""
    <div style="background: white; border-radius: 24px; padding: 48px; box-shadow: 0 20px 25px -5px rgba(0,0,0,0.1), 0 8px 10px -6px rgba(0,0,0,0.1);">
        <div style="text-align: center; margin-bottom: 32px;">
            <div style="font-size: 64px; margin-bottom: 16px;">🏥</div>
            <h1 style="font-size: 28px; font-weight: 700; color: #0D47A1; margin: 0 0 8px 0;">Sistema de Triaje</h1>
            <p style="font-size: 14px; color: #616161; margin: 0;">Hospital Clínico - Unidad de Emergencias</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Formulario de login
    with st.form("login_form"):
        st.markdown("**👤 Usuario**")
        username = st.text_input("Usuario", label_visibility="collapsed", placeholder="Ingrese su usuario")
        
        st.markdown("**🔒 Contraseña**")
        password = st.text_input("Contraseña", type="password", label_visibility="collapsed", placeholder="Ingrese su contraseña")
        
        submitted = st.form_submit_button("🚀 Ingresar al Sistema", use_container_width=True, type="primary")
    
    st.markdown("""
        <p style="text-align: center; margin-top: 24px; font-size: 12px; color: #9E9E9E;">
            © 2024 Hospital Clínico. Todos los derechos reservados.
        </p>
    </div></div>
    """, unsafe_allow_html=True)

    if submitted:
        try:
            resp = requests.post(
                f"{API_BASE_URL}/api/v1/auth/login",
                json={"username": username, "password": password},
                timeout=15,
            )
        except Exception:
            resp = None

        if resp is None:
            st.error("❌ No se pudo conectar al backend. Verifique que el servidor esté corriendo.")
            st.stop()

        if resp.status_code != 200:
            st.error("❌ Usuario o contraseña incorrectos")
            st.stop()

        data = resp.json()
        user = data.get("user") or {}
        token = data.get("accessToken")
        
        # Usar sistema de persistencia robusto
        persist_login(token, user if user else {"username": username})
        st.success("✅ Inicio de sesión exitoso. Bienvenido/a.")
        st.rerun()

if st.session_state.get('authenticated'):
    user_role = st.session_state.get('user_role')
    user_name = st.session_state.get('user_name')
    
    # Sidebar moderno
    with st.sidebar:
        # Header del sidebar
        st.markdown(f"""
        <div style="padding: 20px; border-bottom: 1px solid #EEEEEE; margin-bottom: 16px;">
            <div style="font-size: 20px; font-weight: 700; color: #0D47A1;">🏥 Triaje Clínico</div>
            <div style="font-size: 12px; color: #9E9E9E; margin-top: 4px;">Sistema de Gestión Hospitalaria</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Perfil del usuario
        st.markdown(f"""
        <div style="background: #E3F2FD; border-radius: 12px; padding: 16px; margin-bottom: 20px;">
            <div style="display: flex; align-items: center; gap: 12px;">
                <div style="font-size: 32px;">👤</div>
                <div>
                    <div style="font-size: 14px; font-weight: 600; color: #212121;">{user_name}</div>
                    <div style="font-size: 12px; color: #616161; text-transform: capitalize;">{user_role}</div>
                </div>
            </div>
            <div style="font-size: 11px; color: #9E9E9E; margin-top: 8px; padding-top: 8px; border-top: 1px solid #BBDEFB;">
                📅 {datetime.now().strftime('%d/%m/%Y %H:%M')}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Sección de navegación
        st.markdown("""
        <div style="font-size: 11px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px; color: #9E9E9E; padding: 0 8px; margin-bottom: 8px;">
            Navegación
        </div>
        """, unsafe_allow_html=True)
        
        # Navegación por rol
        if user_role == 'enfermera':
            _nav_link("app.py", label="🏠 Inicio", icon="🏠")
            _nav_link("pages/1_Triage.py", label="📝 Nuevo Triaje", icon="📝")
            _nav_link("pages/3_Dashboard_Op.py", label="📊 Dashboard Operativo", icon="📊")
        elif user_role == 'medico':
            _nav_link("app.py", label="🏠 Inicio", icon="🏠")
            _nav_link("pages/2_Cola_Medica.py", label="🩺 Cola de Atención", icon="🩺")
            _nav_link("pages/3_Dashboard_Op.py", label="📊 Dashboard Operativo", icon="📊")
        else:
            _nav_link("app.py", label="🏠 Inicio", icon="🏠")
            _nav_link("pages/3_Dashboard_Op.py", label="📊 Dashboard", icon="📊")
        
        st.markdown("---")
        
        # Footer con botón de logout
        if st.button("🚪 Cerrar Sesión", use_container_width=True, type="secondary"):
            logout_and_clear()
            st.rerun()
    
    # Main content basado en rol - BIENVENIDA MEJORADA
    if user_role == 'enfermera':
        # --- HEADER ---
        st.markdown('<p style="font-size: 40px; font-weight: bold; color: #2E86C1;">🏥 SISTEMA DE TRIAJE CLÍNICO ASISTIDO POR IA</p>', unsafe_allow_html=True)
        st.caption(f"Hospital Clínico - Unidad de Emergencias | {datetime.now().strftime('%d/%m/%Y %H:%M')}")
        st.markdown("---")
        
        # --- WELCOME SECTION ---
        col_welcome, col_status = st.columns([2, 1])
        
        with col_welcome:
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 30px; border-radius: 15px; color: white;">
                <h2>👋 ¡Bienvenida/o, {user_name}!</h2>
                <p style="font-size: 18px; margin-top: 10px;">
                    Estás en el <strong>Módulo de Enfermería</strong>.<br>
                    Desde aquí puedes registrar nuevos triajes, consultar la cola médica 
                    y revisar el dashboard operativo en tiempo real.
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        with col_status:
            # Cargar datos rápidos del dashboard (hoy por defecto)
            try:
                from utils import obtener_dashboard_operativo
                data = obtener_dashboard_operativo("hoy")
                if data:
                    kpis = data.get('kpis', {})
                    st.markdown(f"""
                    <div style="background: white; padding: 20px; border-radius: 10px; border-left: 5px solid #2E86C1; box-shadow: 0 2px 5px rgba(0,0,0,0.1);">
                        <h4 style="color: #2E86C1; margin: 0;">📊 Estado Actual</h4>
                        <hr style="margin: 10px 0;">
                        <p style="font-size: 24px; font-weight: bold; margin: 0; color: #333;">
                            {kpis.get('en_espera', 0)} <span style="font-size: 14px; font-weight: normal;">en espera</span>
                        </p>
                        <p style="font-size: 24px; font-weight: bold; margin: 0; color: #e74c3c;">
                            {kpis.get('criticos', 0)} <span style="font-size: 14px; font-weight: normal;">críticos</span>
                        </p>
                        <p style="font-size: 14px; color: #666; margin-top: 10px;">
                            ⏱️ Promedio: {kpis.get('tiempo_promedio_min', 0)} min
                        </p>
                    </div>
                    """, unsafe_allow_html=True)
            except:
                st.info("ℹ️ Conectando con el sistema...")
        
        st.markdown("---")
        
        # --- ACTION CARDS ---
        st.subheader("🚀 Acciones Rápidas")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            <div style="background: #f8f9fa; padding: 25px; border-radius: 10px; border: 1px solid #dee2e6;">
                <h3>📝 NUEVO TRIAJE</h3>
                <p style="color: #666; min-height: 50px;">
                    Registrar un nuevo paciente, capturar signos vitales, 
                    documentar síntomas y obtener sugerencia de IA.
                </p>
            </div>
            """, unsafe_allow_html=True)
            if st.button("🚀 Ir a Nuevo Triaje", use_container_width=True, type="primary"):
                st.switch_page("pages/1_Triage.py")
        
        with col2:
            st.markdown("""
            <div style="background: #f8f9fa; padding: 25px; border-radius: 10px; border: 1px solid #dee2e6;">
                <h3>📊 DASHBOARD</h3>
                <p style="color: #666; min-height: 50px;">
                    Ver métricas en tiempo real: pacientes en espera, 
                    tiempo promedio, distribución por urgencia.
                </p>
            </div>
            """, unsafe_allow_html=True)
            if st.button("📈 Ver Dashboard", use_container_width=True):
                st.switch_page("pages/3_Dashboard_Op.py")
        
        with col3:
            st.markdown("""
            <div style="background: #f8f9fa; padding: 25px; border-radius: 10px; border: 1px solid #dee2e6;">
                <h3>🏥 COLA MÉDICA</h3>
                <p style="color: #666; min-height: 50px;">
                    Visualizar la cola de atención médica por nivel de 
                    urgencia (Kanban) y gestionar pacientes.
                </p>
            </div>
            """, unsafe_allow_html=True)
            if st.button("🏥 Ver Cola Médica", use_container_width=True):
                st.switch_page("pages/2_Cola_Medica.py")
            
    elif user_role == 'medico':
        st.title("🩺 Panel de Atención Médica")
        st.markdown("### Bienvenido/a, Dr/a.")
        st.info("""
        **Acciones disponibles:**
        - 🩺 **Cola de Atención**: Visualiza pacientes en espera y gestiona el flujo
        - 📊 **Dashboard operativo**: Monitorea métricas de la unidad
        
        *Solo tú puedes cambiar estados logísticos y agregar diagnósticos finales.*
        """)
        
        # Mostrar resumen de cola actual
        try:
            response = requests.get(f"{API_BASE_URL}/api/v1/cola-medica/")
            if response.status_code == 200:
                cola = response.json()
                en_espera = len([p for p in cola if p['estado_logistico'] == 'En Espera'])
                en_atencion = len([p for p in cola if p['estado_logistico'] == 'En Atencion'])
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("⏳ En Espera", en_espera)
                with col2:
                    st.metric("🩺 En Atención", en_atencion)
                with col3:
                    criticos = len([p for p in cola if p['nivel_urgencia_final'] in ['RED', 'ORANGE'] and p['estado_logistico'] == 'En Espera'])
                    st.metric("🔴 Críticos en espera", criticos, delta="Prioridad máxima" if criticos > 0 else None)
        except:
            st.warning("No se pudo cargar el estado de la cola")
            
    else:  # gerente
        st.title("📊 Panel de Gestión")
        st.markdown("### Bienvenido/a, Gerente")
        st.info("""
        **Acciones disponibles:**
        - 📊 **Dashboard operativo**: Visualiza KPIs y reportes
        - Los reportes detallados están disponibles en la aplicación React de gestión
        """)