"""
Componentes de modales para el Sistema de Triaje Clínico
Diálogos, confirmaciones y formularios modales
"""

import streamlit as st
from typing import Optional, Callable, List, Dict, Any


class UIModal:
    """Sistema de modales reutilizables"""
    
    @staticmethod
    def justify_return_modal(
        patient_name: str,
        patient_id: str,
        on_submit: Optional[Callable[[str], None]] = None,
        on_cancel: Optional[Callable] = None,
        key: str = "justify_return"
    ) -> Optional[str]:
        """
        Modal para justificar la devolución de un paciente
        
        Args:
            patient_name: Nombre del paciente
            patient_id: ID del paciente
            on_submit: Callback con el motivo de devolución
            on_cancel: Callback al cancelar
            key: Key única para el modal
            
        Returns:
            El motivo ingresado si se confirma, None si se cancela
        """
        with st.container():
            st.markdown(f"""
            <div class="modal-overlay" id="{key}_overlay">
                <div class="modal-content">
                    <div class="modal-header">
                        <h3 class="modal-title">↩️ Devolver Paciente</h3>
                    </div>
                    <div class="modal-body">
                        <p><strong>Paciente:</strong> {patient_name}</p>
                        <p><strong>ID:</strong> {patient_id}</p>
                        <p style="margin-top: 16px; margin-bottom: 8px;">
                            Por favor, indique el motivo de la devolución:
                        </p>
            """, unsafe_allow_html=True)
            
            # Input de texto
            motivo = st.text_area(
                "Motivo de devolución",
                key=f"{key}_motivo",
                placeholder="Ej: Paciente no se presentó, información incompleta, etc.",
                height=100
            )
            
            st.markdown("""
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Botones
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("✕ Cancelar", key=f"{key}_cancel", use_container_width=True):
                    if on_cancel:
                        on_cancel()
                    st.session_state[f"{key}_open"] = False
                    st.rerun()
            
            with col2:
                submit_disabled = not motivo or len(motivo.strip()) < 5
                if st.button(
                    "✓ Confirmar Devolución",
                    key=f"{key}_submit",
                    type="primary",
                    disabled=submit_disabled,
                    use_container_width=True
                ):
                    if on_submit:
                        on_submit(motivo)
                    st.session_state[f"{key}_open"] = False
                    st.rerun()
            
            return motivo if (motivo and len(motivo.strip()) >= 5) else None
    
    @staticmethod
    def confirm_action_modal(
        title: str,
        message: str,
        confirm_label: str = "Confirmar",
        cancel_label: str = "Cancelar",
        confirm_variant: str = "primary",
        danger: bool = False,
        on_confirm: Optional[Callable] = None,
        on_cancel: Optional[Callable] = None,
        key: str = "confirm_action"
    ) -> bool:
        """
        Modal de confirmación genérico
        
        Args:
            title: Título del modal
            message: Mensaje descriptivo
            confirm_label: Texto del botón confirmar
            cancel_label: Texto del botón cancelar
            confirm_variant: Variante del botón confirmar
            danger: Si es una acción peligrosa (cambia colores)
            on_confirm: Callback al confirmar
            on_cancel: Callback al cancelar
            key: Key única
            
        Returns:
            True si se confirmó, False si se canceló
        """
        icon = "⚠️" if danger else "❓"
        
        st.markdown(f"""
        <div class="modal-overlay" id="{key}_overlay">
            <div class="modal-content">
                <div class="modal-header">
                    <h3 class="modal-title">{icon} {title}</h3>
                </div>
                <div class="modal-body">
                    <p>{message}</p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        confirmed = False
        
        with col1:
            if st.button(cancel_label, key=f"{key}_cancel", use_container_width=True):
                if on_cancel:
                    on_cancel()
                confirmed = False
                st.session_state[f"{key}_result"] = False
                st.rerun()
        
        with col2:
            button_type = "primary" if not danger else "secondary"
            if st.button(
                confirm_label,
                key=f"{key}_confirm",
                type=button_type,
                use_container_width=True
            ):
                if on_confirm:
                    on_confirm()
                confirmed = True
                st.session_state[f"{key}_result"] = True
                st.rerun()
        
        return confirmed
    
    @staticmethod
    def patient_details_modal(
        patient_data: Dict[str, Any],
        on_close: Optional[Callable] = None,
        key: str = "patient_details"
    ) -> None:
        """
        Modal para mostrar detalles de paciente
        
        Args:
            patient_data: Diccionario con datos del paciente
            on_close: Callback al cerrar
            key: Key única
        """
        st.markdown(f"""
        <div class="modal-overlay" id="{key}_overlay">
            <div class="modal-content" style="max-width: 600px;">
                <div class="modal-header">
                    <h3 class="modal-title">👤 Detalles del Paciente</h3>
                </div>
                <div class="modal-body">
        """, unsafe_allow_html=True)
        
        # Mostrar datos del paciente
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Información Personal**")
            st.write(f"**Nombre:** {patient_data.get('nombres', '')} {patient_data.get('apellidos', '')}")
            st.write(f"**DNI:** {patient_data.get('dni', 'N/A')}")
            st.write(f"**Edad:** {patient_data.get('edad', 'N/A')} años")
            st.write(f"**Sexo:** {patient_data.get('sexo', 'N/A')}")
        
        with col2:
            st.markdown("**Información de Contacto**")
            st.write(f"**Teléfono:** {patient_data.get('telefono', 'N/A')}")
            st.write(f"**Email:** {patient_data.get('email', 'N/A')}")
            st.write(f"**Dirección:** {patient_data.get('direccion', 'N/A')}")
        
        # Historial de triajes si existe
        if 'triajes' in patient_data and patient_data['triajes']:
            st.markdown("---")
            st.markdown("**Historial de Triajes**")
            for triaje in patient_data['triajes']:
                with st.expander(f"Triaje #{triaje.get('id', 'N/A')} - {triaje.get('fecha', 'N/A')}"):
                    st.write(f"**Motivo:** {triaje.get('motivo_consulta', 'N/A')}")
                    st.write(f"**Nivel de Urgencia:** {triaje.get('nivel_urgencia_final', 'N/A')}")
                    st.write(f"**Estado:** {triaje.get('estado', 'N/A')}")
        
        st.markdown("""
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("✕ Cerrar", key=f"{key}_close", use_container_width=True):
            if on_close:
                on_close()
            st.rerun()


class AlertModal:
    """Modales de alerta predefinidos"""
    
    @staticmethod
    def success(
        message: str,
        title: str = "Éxito",
        on_close: Optional[Callable] = None,
        key: str = "alert_success"
    ) -> None:
        """Modal de éxito"""
        st.success(f"✓ {title}: {message}")
        if on_close:
            if st.button("Aceptar", key=f"{key}_close"):
                on_close()
                st.rerun()
    
    @staticmethod
    def error(
        message: str,
        title: str = "Error",
        on_close: Optional[Callable] = None,
        key: str = "alert_error"
    ) -> None:
        """Modal de error"""
        st.error(f"✕ {title}: {message}")
        if on_close:
            if st.button("Aceptar", key=f"{key}_close"):
                on_close()
                st.rerun()
    
    @staticmethod
    def warning(
        message: str,
        title: str = "Advertencia",
        on_close: Optional[Callable] = None,
        key: str = "alert_warning"
    ) -> None:
        """Modal de advertencia"""
        st.warning(f"⚠️ {title}: {message}")
        if on_close:
            if st.button("Aceptar", key=f"{key}_close"):
                on_close()
                st.rerun()
    
    @staticmethod
    def info(
        message: str,
        title: str = "Información",
        on_close: Optional[Callable] = None,
        key: str = "alert_info"
    ) -> None:
        """Modal informativo"""
        st.info(f"ℹ️ {title}: {message}")
        if on_close:
            if st.button("Aceptar", key=f"{key}_close"):
                on_close()
                st.rerun()


class FormModal:
    """Modales con formularios"""
    
    @staticmethod
    def quick_note_modal(
        patient_id: str,
        on_submit: Optional[Callable[[str], None]] = None,
        on_cancel: Optional[Callable] = None,
        key: str = "quick_note"
    ) -> Optional[str]:
        """
        Modal para agregar nota rápida
        
        Returns:
            El texto de la nota si se envía, None si se cancela
        """
        st.markdown(f"""
        <div class="modal-overlay" id="{key}_overlay">
            <div class="modal-content">
                <div class="modal-header">
                    <h3 class="modal-title">📝 Agregar Nota</h3>
                </div>
                <div class="modal-body">
        """, unsafe_allow_html=True)
        
        nota = st.text_area(
            "Nota",
            key=f"{key}_text",
            placeholder="Ingrese su nota aquí...",
            height=100
        )
        
        st.markdown("""
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("Cancelar", key=f"{key}_cancel", use_container_width=True):
                if on_cancel:
                    on_cancel()
                st.rerun()
        
        with col2:
            if st.button("Guardar Nota", key=f"{key}_submit", type="primary", use_container_width=True):
                if on_submit and nota:
                    on_submit(nota)
                st.rerun()
        
        return nota
    
    @staticmethod
    def change_urgency_modal(
        patient_id: str,
        current_level: str,
        available_levels: List[str],
        on_submit: Optional[Callable[[str, str], None]] = None,
        on_cancel: Optional[Callable] = None,
        key: str = "change_urgency"
    ) -> Optional[tuple]:
        """
        Modal para cambiar nivel de urgencia con justificación
        
        Returns:
            Tupla (nuevo_nivel, justificacion) si se confirma, None si se cancela
        """
        st.markdown(f"""
        <div class="modal-overlay" id="{key}_overlay">
            <div class="modal-content">
                <div class="modal-header">
                    <h3 class="modal-title">🔄 Cambiar Nivel de Urgencia</h3>
                </div>
                <div class="modal-body">
                    <p><strong>Nivel actual:</strong> {current_level}</p>
        """, unsafe_allow_html=True)
        
        nuevo_nivel = st.selectbox(
            "Nuevo nivel de urgencia",
            options=available_levels,
            key=f"{key}_level"
        )
        
        justificacion = st.text_area(
            "Justificación del cambio *",
            key=f"{key}_justif",
            placeholder="Explique por qué se realiza el cambio de nivel...",
            height=80
        )
        
        st.markdown("""
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        result = None
        
        with col1:
            if st.button("Cancelar", key=f"{key}_cancel", use_container_width=True):
                if on_cancel:
                    on_cancel()
                st.rerun()
        
        with col2:
            can_submit = justificacion and len(justificacion.strip()) >= 10
            if st.button(
                "Confirmar Cambio",
                key=f"{key}_submit",
                type="primary",
                disabled=not can_submit,
                use_container_width=True
            ):
                if on_submit:
                    on_submit(nuevo_nivel, justificacion)
                result = (nuevo_nivel, justificacion)
                st.rerun()
        
        return result


# Helper functions para uso directo
def modal_justify_return(patient_name: str, patient_id: str, **kwargs) -> Optional[str]:
    """Helper para modal de justificación de devolución"""
    return UIModal.justify_return_modal(patient_name, patient_id, **kwargs)

def modal_confirm(
    title: str,
    message: str,
    **kwargs
) -> bool:
    """Helper para modal de confirmación"""
    return UIModal.confirm_action_modal(title, message, **kwargs)

def modal_patient_details(patient_data: Dict[str, Any], **kwargs) -> None:
    """Helper para modal de detalles de paciente"""
    UIModal.patient_details_modal(patient_data, **kwargs)

def alert_success(message: str, **kwargs) -> None:
    """Helper para alerta de éxito"""
    AlertModal.success(message, **kwargs)

def alert_error(message: str, **kwargs) -> None:
    """Helper para alerta de error"""
    AlertModal.error(message, **kwargs)

def alert_warning(message: str, **kwargs) -> None:
    """Helper para alerta de advertencia"""
    AlertModal.warning(message, **kwargs)

def alert_info(message: str, **kwargs) -> None:
    """Helper para alerta informativa"""
    AlertModal.info(message, **kwargs)

def modal_quick_note(patient_id: str, **kwargs) -> Optional[str]:
    """Helper para modal de nota rápida"""
    return FormModal.quick_note_modal(patient_id, **kwargs)

def modal_change_urgency(patient_id: str, current_level: str, available_levels: List[str], **kwargs) -> Optional[tuple]:
    """Helper para modal de cambio de urgencia"""
    return FormModal.change_urgency_modal(patient_id, current_level, available_levels, **kwargs)
