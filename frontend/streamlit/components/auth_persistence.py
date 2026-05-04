"""
Componente para persistencia de autenticación usando archivo temporal
"""
import streamlit as st
import base64
import requests
import json
import os
from datetime import datetime, timedelta

# Archivo donde guardar el token
def get_token_file():
    """Retorna ruta del archivo de token"""
    import tempfile
    return os.path.join(tempfile.gettempdir(), "triage_auth_token.json")

def save_token_to_file(token: str, user: dict):
    """Guarda token en archivo temporal"""
    try:
        data = {
            "token": token,
            "user": user,
            "timestamp": datetime.now().isoformat(),
            "expires": (datetime.now() + timedelta(hours=8)).isoformat()  # 8 horas
        }
        with open(get_token_file(), 'w') as f:
            json.dump(data, f)
    except Exception as e:
        print(f"Error guardando token: {e}")

def load_token_from_file():
    """Carga token desde archivo temporal"""
    try:
        file_path = get_token_file()
        if not os.path.exists(file_path):
            return None
        
        with open(file_path, 'r') as f:
            data = json.load(f)
        
        # Verificar expiración
        expires = datetime.fromisoformat(data.get('expires', '2000-01-01'))
        if datetime.now() > expires:
            os.remove(file_path)
            return None
        
        return data
    except Exception as e:
        print(f"Error cargando token: {e}")
        return None

def clear_token_file():
    """Elimina archivo de token"""
    try:
        file_path = get_token_file()
        if os.path.exists(file_path):
            os.remove(file_path)
    except:
        pass

def get_auth_storage_key():
    """Retorna la clave única para almacenar el token"""
    return "triage_ia_auth_token"

def init_auth_storage():
    """Inicializa el componente de almacenamiento en el frontend"""
    # Usar componente HTML con JavaScript para acceder a localStorage
    st.components.v1.html("""
    <script>
    // Función para guardar token en localStorage
    window.saveAuthToken = function(token) {
        localStorage.setItem('triage_ia_auth_token', token);
        localStorage.setItem('triage_ia_auth_timestamp', Date.now().toString());
        return true;
    };
    
    // Función para obtener token de localStorage
    window.getAuthToken = function() {
        return localStorage.getItem('triage_ia_auth_token');
    };
    
    // Función para eliminar token
    window.clearAuthToken = function() {
        localStorage.removeItem('triage_ia_auth_token');
        localStorage.removeItem('triage_ia_auth_timestamp');
        return true;
    };
    
    // Comunicar con Streamlit
    const token = localStorage.getItem('triage_ia_auth_token');
    if (token) {
        window.parent.postMessage({
            type: 'streamlit:setComponentValue',
            value: {auth_token: token, source: 'localStorage'}
        }, '*');
    }
    </script>
    """, height=0)

def save_token_to_storage(token: str):
    """Guarda el token en localStorage vía JavaScript"""
    if not token:
        return
    
    # Codificar token para seguridad básica
    encoded = base64.b64encode(token.encode()).decode()
    
    st.components.v1.html(f"""
    <script>
    localStorage.setItem('triage_ia_auth_token', '{encoded}');
    localStorage.setItem('triage_ia_auth_timestamp', Date.now().toString());
    </script>
    """, height=0)
    
    # También guardar en session_state como backup
    st.session_state['stored_token'] = encoded

def get_token_from_storage() -> str:
    """Recupera el token de localStorage o session_state"""
    # Primero intentar session_state (persiste durante la sesión del navegador)
    encoded = st.session_state.get('stored_token')
    if encoded:
        try:
            return base64.b64decode(encoded.encode()).decode()
        except:
            pass
    
    # Intentar obtener de query params (método actual)
    if hasattr(st, "query_params"):
        qp = st.query_params
    else:
        qp = st.experimental_get_query_params()
    
    if isinstance(qp.get("token"), list):
        token = (qp.get("token") or [None])[0]
    else:
        token = qp.get("token")
    
    return token

def clear_token_storage():
    """Limpia el token de todas las ubicaciones"""
    st.components.v1.html("""
    <script>
    localStorage.removeItem('triage_ia_auth_token');
    localStorage.removeItem('triage_ia_auth_timestamp');
    </script>
    """, height=0)
    
    if 'stored_token' in st.session_state:
        del st.session_state['stored_token']
    if 'api_token' in st.session_state:
        del st.session_state['api_token']
    if 'authenticated' in st.session_state:
        del st.session_state['authenticated']

# Función para sincronizar token desde localStorage al cargar la página
def sync_token_from_storage():
    """Componente que sincroniza token desde localStorage al session_state"""
    # Crear placeholder para recibir token desde JS
    if 'localstorage_token' not in st.session_state:
        st.session_state['localstorage_token'] = None
    
    # Componente que lee de localStorage y envía a Streamlit
    token_placeholder = st.components.v1.html("""
    <div id="auth-sync" style="display:none;"></div>
    <script>
    (function() {
        const token = localStorage.getItem('triage_ia_auth_token');
        const container = document.getElementById('auth-sync');
        if (token) {
            container.setAttribute('data-token', token);
            // Enviar mensaje a Streamlit
            window.parent.postMessage({
                type: 'streamlit:componentReady',
                token: token
            }, '*');
        }
    })();
    </script>
    """, height=0)
    
    return token_placeholder

def restore_session_from_storage():
    """
    Intenta restaurar la sesión desde cualquier fuente disponible.
    Retorna True si se restauró exitosamente.
    """
    # Si ya está autenticado, no hacer nada
    if st.session_state.get('authenticated') and st.session_state.get('api_token'):
        return True
    
    # 1. Intentar recuperar desde archivo (persiste entre refrescos)
    file_data = load_token_from_file()
    if file_data:
        token = file_data.get('token')
        user = file_data.get('user', {})
        if token:
            st.session_state['api_token'] = token
            st.session_state['user'] = user
            # Guardar backup en session_state también
            st.session_state['stored_token'] = base64.b64encode(token.encode()).decode()
            return True
    
    # 2. Intentar recuperar token de session_state (backup)
    encoded_token = st.session_state.get('stored_token')
    if encoded_token:
        try:
            token = base64.b64decode(encoded_token.encode()).decode()
            st.session_state['api_token'] = token
            return True
        except:
            pass
    
    # 3. Intentar recuperar de query params
    if hasattr(st, "query_params"):
        qp = st.query_params
    else:
        qp = st.experimental_get_query_params()
    
    if isinstance(qp.get("token"), list):
        token = (qp.get("token") or [None])[0]
    else:
        token = qp.get("token")
    
    if token:
        st.session_state['api_token'] = token
        # Guardar backup para futuras recuperaciones
        st.session_state['stored_token'] = base64.b64encode(token.encode()).decode()
        return True
    
    return False

def verify_and_restore_session(api_base_url: str):
    """
    Verifica el token con el backend y restaura la sesión completa.
    Retorna True si la sesión fue restaurada exitosamente.
    """
    import requests
    
    # Primero intentar restaurar el token desde storage
    if not restore_session_from_storage():
        return False
    
    token = st.session_state.get('api_token')
    if not token:
        return False
    
    # Verificar token con el backend
    try:
        me_resp = requests.get(
            f"{api_base_url}/api/v1/auth/me",
            headers={"Authorization": f"Bearer {token}"},
            timeout=15,
        )
        
        if me_resp.status_code == 200:
            user = me_resp.json() or {}
            st.session_state['authenticated'] = True
            st.session_state['username'] = user.get("username")
            st.session_state['user_role'] = user.get("rol")
            st.session_state['user_name'] = f"{user.get('nombres', '')} {user.get('apellidos', '')}".strip() or user.get("username")
            return True
    except Exception as e:
        print(f"Error verificando token: {e}")
    
    # Token inválido, limpiar
    clear_token_storage()
    return False

def persist_login(token: str, user_data: dict):
    """
    Persiste el login en múltiples capas para máxima confiabilidad.
    """
    import base64
    
    # 1. Guardar en session_state
    st.session_state['authenticated'] = True
    st.session_state['api_token'] = token
    st.session_state['username'] = user_data.get("username")
    st.session_state['user_role'] = user_data.get("rol")
    st.session_state['user_name'] = f"{user_data.get('nombres', '')} {user_data.get('apellidos', '')}".strip() or user_data.get("username")
    st.session_state['user'] = user_data
    
    # 2. Guardar en query params (URL)
    if hasattr(st, "query_params"):
        st.query_params['token'] = token
    else:
        st.experimental_set_query_params(token=token)
    
    # 3. Guardar encoded backup en session_state
    st.session_state['stored_token'] = base64.b64encode(token.encode()).decode()
    
    # 4. Guardar en archivo (persiste entre refrescos de página)
    save_token_to_file(token, user_data)
    
    # 5. Intentar guardar en localStorage
    try:
        encoded = base64.b64encode(token.encode()).decode()
        st.components.v1.html(f"""
        <script>
        localStorage.setItem('triage_ia_auth_token', '{encoded}');
        localStorage.setItem('triage_ia_auth_timestamp', Date.now().toString());
        </script>
        """, height=0)
    except:
        pass

def logout_and_clear():
    """Limpia todas las formas de persistencia"""
    # Limpiar archivo de token
    clear_token_file()
    
    # Limpiar localStorage
    try:
        st.components.v1.html("""
        <script>
        localStorage.removeItem('triage_ia_auth_token');
        localStorage.removeItem('triage_ia_auth_timestamp');
        </script>
        """, height=0)
    except:
        pass
    
    # Limpiar query params
    try:
        if hasattr(st, "query_params"):
            st.query_params.clear()
        else:
            st.experimental_set_query_params()
    except:
        pass
    
    # Limpiar session_state
    keys_to_clear = ['authenticated', 'api_token', 'username', 'user_role', 'user_name', 'stored_token', 'localstorage_token', 'user']
    for key in keys_to_clear:
        if key in st.session_state:
            del st.session_state[key]
