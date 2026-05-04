import streamlit as st
import requests
from utils import get_auth_headers

def paciente_search_component(key_prefix: str = ""):
    """Componente reutilizable para búsqueda de pacientes"""
    
    st.markdown("### 🔍 Buscar Paciente")
    
    col1, col2 = st.columns([3, 1])
    with col1:
        search_term = st.text_input(
            "DNI o Nombre",
            key=f"search_{key_prefix}",
            placeholder="Ej: 12345678A o María"
        )
    with col2:
        st.markdown("####")
        if st.button("🔍 Buscar", key=f"btn_search_{key_prefix}"):
            return search_term
    
    return None

def paciente_info_card(paciente: dict):
    """Muestra tarjeta de información del paciente"""
    
    from datetime import date
    hoy = date.today()
    edad = hoy.year - paciente['fecha_nacimiento'].year - (
        (hoy.month, hoy.day) < (paciente['fecha_nacimiento'].month, paciente['fecha_nacimiento'].day)
    )
    
    st.markdown(f"""
    <div style="background-color: #f0f9ff; padding: 15px; border-radius: 10px; border-left: 5px solid #2E86C1; margin-bottom: 15px;">
        <strong>📋 Datos del Paciente</strong><br>
        {paciente['nombres']} {paciente['apellidos']}<br>
        DNI: {paciente['dni']} | Edad: {edad} años<br>
        📞 {paciente.get('telefono', 'No registrado')}
    </div>
    """, unsafe_allow_html=True)