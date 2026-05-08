import streamlit as st
import requests
import json
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
import os

# Configuración de la API - Usar variable de entorno o valor por defecto
# Normalizar para evitar duplicación de /api/v1
_raw_url = os.getenv("API_BASE_URL", "http://localhost:8000/api/v1")
# Remover /api/v1 del final si existe, luego agregarlo una sola vez
API_BASE_URL = _raw_url.rstrip("/").removesuffix("/api/v1") + "/api/v1"

def get_auth_headers():
    """Retorna headers con token JWT si está disponible en session_state"""
    token = st.session_state.get('api_token')
    if token:
        return {"Authorization": f"Bearer {token}"}
    return {}

def is_authenticated() -> bool:
    """Verifica si hay token válido en session_state"""
    return bool(st.session_state.get('api_token'))

def logout():
    """Cierra sesión eliminando token de session_state"""
    keys_to_remove = ['api_token', 'authenticated', 'username', 'user_role', 'user_name', 'stored_token']
    for key in keys_to_remove:
        if key in st.session_state:
            del st.session_state[key]

def api_login(username: str, password: str) -> Optional[Dict]:
    """Realiza login contra FastAPI y retorna datos (sin guardar en session)"""
    try:
        response = requests.post(
            f"{API_BASE_URL}/auth/login",
            json={"username": username, "password": password},
            timeout=10
        )
        if response.status_code == 200:
            return response.json()
        else:
            return None
    except Exception as e:
        st.error(f"Error conectando al servidor: {str(e)}")
        return None

def buscar_paciente(search_term: str) -> Optional[Dict]:
    """Busca paciente por DNI o nombre"""
    headers = get_auth_headers()
    try:
        response = requests.get(
            f"{API_BASE_URL}/pacientes/",
            params={"search": search_term, "limit": 5},
            headers=headers,
            timeout=10
        )
        if response.status_code == 200:
            pacientes = response.json()
            if pacientes:
                return pacientes[0]
        return None
    except:
        return None

def crear_paciente(paciente_data: Dict) -> Optional[Dict]:
    """Crea un nuevo paciente"""
    headers = get_auth_headers()
    try:
        response = requests.post(
            f"{API_BASE_URL}/pacientes/",
            json=paciente_data,
            headers=headers,
            timeout=10
        )
        if response.status_code == 201:
            return response.json()
        else:
            st.error(f"Error creando paciente: {response.text}")
            return None
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return None

def crear_triaje(triaje_data: Dict) -> Optional[Dict]:
    """Crea un nuevo triaje con evaluación IA"""
    headers = get_auth_headers()
    try:
        response = requests.post(
            f"{API_BASE_URL}/triaje/",
            json=triaje_data,
            headers=headers,
            timeout=30
        )
        if response.status_code == 201:
            return response.json()
        elif response.status_code == 503:
            st.warning("⚠️ Servicio IA no disponible. El triaje se registró con nivel por defecto. Por favor revise manualmente.")
            return response.json() if response.text else None
        else:
            st.error(f"Error: {response.text}")
            return None
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return None

def confirmar_nivel_urgencia(triaje_id: int, nivel_final: str) -> bool:
    """Confirma o sobreescribe el nivel de urgencia"""
    headers = get_auth_headers()
    try:
        response = requests.put(
            f"{API_BASE_URL}/triaje/{triaje_id}/confirmar",
            params={"nivel_final": nivel_final},
            headers=headers,
            timeout=10
        )
        return response.status_code == 200
    except:
        return False

def cambiar_estado_triaje(triaje_id: int, nuevo_estado: str, justificacion: str = None, version: int = None) -> tuple:
    """Cambia estado logístico con optimistic locking"""
    headers = get_auth_headers()
    payload = {
        "nuevo_estado": nuevo_estado,
        "version_actual": version
    }
    if justificacion:
        payload["justificacion"] = justificacion
    
    try:
        response = requests.put(
            f"{API_BASE_URL}/cola-medica/{triaje_id}/estado",
            json=payload,
            headers=headers,
            timeout=10
        )
        if response.status_code == 200:
            return True, response.json().get('message', 'Éxito')
        elif response.status_code == 409:
            return False, "CONFLICTO: El registro fue modificado por otro usuario. Por favor recargue."
        else:
            return False, response.json().get('detail', 'Error desconocido')
    except Exception as e:
        return False, str(e)

def obtener_antecedentes_hce(paciente_id: int) -> Optional[Dict]:
    """Obtiene antecedentes HCE simulados"""
    headers = get_auth_headers()
    try:
        response = requests.get(
            f"{API_BASE_URL}/hce/{paciente_id}",
            headers=headers,
            timeout=10
        )
        if response.status_code == 200:
            return response.json()
        return None
    except:
        return None

def get_color_for_urgency(level: str) -> str:
    """Retorna color HTML para nivel de urgencia"""
    colors = {
        "RED": "#FF0000",
        "ORANGE": "#FFA500",
        "YELLOW": "#FFFF00",
        "GREEN": "#00FF00",
        "BLUE": "#0000FF"
    }
    return colors.get(level, "#CCCCCC")

def get_urgency_label(level: str) -> str:
    """Retorna etiqueta legible para nivel de urgencia"""
    labels = {
        "RED": "🔴 Crítico",
        "ORANGE": "🟠 Urgente",
        "YELLOW": "🟡 Poco Urgente",
        "GREEN": "🟢 No Urgente",
        "BLUE": "🔵 Administrativo"
    }
    return labels.get(level, level)

# ============================================
# FUNCIÓN CORREGIDA - Usa el endpoint correcto
# ============================================
def obtener_dashboard_operativo(rango: str = "hoy") -> Optional[Dict]:
    """
    Obtiene datos en tiempo real para el dashboard operativo de enfermería
    
    Args:
        rango: "hoy", "mes", o "total"
    """
    headers = get_auth_headers()
    
    try:
        # Usar el endpoint correcto: /dashboard-operativo (no /dashboard)
        url = f"{API_BASE_URL}/reportes/dashboard-operativo"
        params = {"rango": rango}  # Parámetro 'rango', no fechas
        
        response = requests.get(
            url,
            headers=headers,
            params=params,
            timeout=10
        )
        
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 403:
            st.error("⚠️ Acceso denunciado. El dashboard operativo requiere rol de enfermería.")
            return None
        else:
            st.error(f"Error {response.status_code}: {response.text}")
            return None
    except requests.exceptions.Timeout:
        st.error("Error: Tiempo de espera agotado. El servidor no responde.")
        return None
    except requests.exceptions.ConnectionError:
        st.error("Error: No se puede conectar al servidor. Verifica que el backend esté corriendo.")
        return None
    except Exception as e:
        st.error(f"Error cargando dashboard: {str(e)}")
        return None

def obtener_cola_medica() -> Optional[list]:
    """Obtiene la lista de pacientes en cola médica"""
    headers = get_auth_headers()
    try:
        response = requests.get(
            f"{API_BASE_URL}/cola-medica/",
            headers=headers,
            timeout=10
        )
        if response.status_code == 200:
            return response.json()
        return None
    except Exception as e:
        st.error(f"Error cargando cola médica: {str(e)}")
        return None

def obtener_triajes_paciente(paciente_id: int) -> Optional[list]:
    """Obtiene el historial de triajes de un paciente"""
    headers = get_auth_headers()
    try:
        response = requests.get(
            f"{API_BASE_URL}/triajes/paciente/{paciente_id}",
            headers=headers,
            timeout=10
        )
        if response.status_code == 200:
            return response.json()
        return None
    except Exception as e:
        st.error(f"Error cargando historial: {str(e)}")
        return None