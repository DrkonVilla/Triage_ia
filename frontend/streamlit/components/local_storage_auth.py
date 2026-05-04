"""
Autenticación persistente usando localStorage del navegador.
Esta es la única forma confiable de persistir sesión en Streamlit.
"""
import streamlit as st
import json

def init_local_storage():
    """
    Inicializa el sistema de localStorage.
    Llama esto al inicio de cada página.
    """
    # Componente que lee de localStorage y lo pone en session_state
    # También escucha cambios y sincroniza
    st.components.v1.html("""
    <script>
    // Leer token de localStorage
    const token = localStorage.getItem('triage_auth_token');
    const user = localStorage.getItem('triage_auth_user');
    
    if (token && user) {
        // Enviar a Streamlit via postMessage
        window.parent.postMessage({
            type: 'streamlit:token',
            token: token,
            user: JSON.parse(user)
        }, '*');
    }
    
    // Escuchar mensajes de Streamlit para guardar token
    window.addEventListener('message', function(event) {
        if (event.data.type === 'saveToken') {
            localStorage.setItem('triage_auth_token', event.data.token);
            localStorage.setItem('triage_auth_user', JSON.stringify(event.data.user));
            localStorage.setItem('triage_auth_time', Date.now().toString());
        }
        if (event.data.type === 'clearToken') {
            localStorage.removeItem('triage_auth_token');
            localStorage.removeItem('triage_auth_user');
            localStorage.removeItem('triage_auth_time');
        }
    });
    </script>
    """, height=0)
    
    # Verificar si hay token en session_state (puesto por el callback de arriba)
    # Nota: Streamlit no puede recibir postMessage directamente de forma simple
    # Por eso usamos un enfoque diferente: hidden input

def save_token_to_browser(token: str, user: dict):
    """Guarda token en localStorage del navegador"""
    user_json = json.dumps(user).replace('"', '\\"')
    st.components.v1.html(f"""
    <script>
    localStorage.setItem('triage_auth_token', '{token}');
    localStorage.setItem('triage_auth_user', "{user_json}");
    localStorage.setItem('triage_auth_time', Date.now().toString());
    </script>
    """, height=0)
    
    # También guardar en session_state como backup
    st.session_state['api_token'] = token
    st.session_state['user'] = user
    st.session_state['authenticated'] = True

def clear_browser_token():
    """Limpia token de localStorage"""
    st.components.v1.html("""
    <script>
    localStorage.removeItem('triage_auth_token');
    localStorage.removeItem('triage_auth_user');
    localStorage.removeItem('triage_auth_time');
    </script>
    """, height=0)
    
    # Limpiar session_state
    for key in ['api_token', 'user', 'authenticated', 'username', 'user_role', 'user_name']:
        if key in st.session_state:
            del st.session_state[key]

def check_and_restore_auth():
    """
    Verifica si hay autenticación guardada y la restaura.
    Retorna True si se restauró exitosamente.
    """
    # Si ya está autenticado en session_state, todo bien
    if st.session_state.get('authenticated') and st.session_state.get('api_token'):
        return True
    
    # Si hay token en session_state pero no autenticado, marcar como autenticado
    if st.session_state.get('api_token') and st.session_state.get('user'):
        st.session_state['authenticated'] = True
        user = st.session_state['user']
        st.session_state['username'] = user.get('username')
        st.session_state['user_role'] = user.get('rol')
        st.session_state['user_name'] = f"{user.get('nombres', '')} {user.get('apellidos', '')}".strip() or user.get('username')
        return True
    
    return False

# Función principal para usar en cada página
def ensure_auth(api_base_url: str = "http://localhost:8000"):
    """
    Asegura que el usuario esté autenticado.
    Si no lo está, muestra mensaje de error.
    """
    import requests
    
    # Inicializar localStorage
    init_local_storage()
    
    # Verificar si ya está autenticado
    if check_and_restore_auth():
        return True
    
    # Si no está autenticado, mostrar error
    return False
