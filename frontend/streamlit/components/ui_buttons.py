"""
Componentes de botones estilizados para el Sistema de Triaje Clínico
Botones con diferentes jerarquías, iconos y estados
"""

import streamlit as st
from typing import Optional, Callable, Literal


ButtonVariant = Literal["primary", "secondary", "success", "warning", "danger", "outline", "ghost"]
ButtonSize = Literal["sm", "md", "lg"]


class UIButton:
    """Sistema de botones con jerarquía visual"""
    
    @staticmethod
    def render(
        label: str,
        key: Optional[str] = None,
        variant: ButtonVariant = "primary",
        size: ButtonSize = "md",
        icon: Optional[str] = None,
        disabled: bool = False,
        full_width: bool = False,
        on_click: Optional[Callable] = None,
        help: Optional[str] = None
    ) -> bool:
        """
        Renderiza un botón estilizado
        
        Args:
            label: Texto del botón
            key: Key única para Streamlit
            variant: Variante visual (primary, secondary, success, warning, danger, outline, ghost)
            size: Tamaño (sm, md, lg)
            icon: Emoji/icono opcional
            disabled: Si está deshabilitado
            full_width: Si ocupa todo el ancho disponible
            on_click: Callback al hacer click
            help: Tooltip de ayuda
            
        Returns:
            True si fue clickeado
        """
        # Mapeo de variantes a tipos de botón de Streamlit
        type_mapping = {
            "primary": "primary",
            "secondary": "secondary",
            "success": "primary",
            "warning": "primary",
            "danger": "primary",
            "outline": "secondary",
            "ghost": "secondary"
        }
        
        button_type = type_mapping.get(variant, "primary")
        
        # Preparar label con icono
        button_label = f"{icon} {label}" if icon else label
        
        # CSS adicional según variante
        css_class = f"btn-{variant}"
        
        button_kwargs = {
            "key": key or f"btn_{label}_{variant}",
            "type": button_type,
            "disabled": disabled,
            "help": help,
            "use_container_width": full_width
        }
        
        clicked = st.button(button_label, **button_kwargs)
        
        if clicked and on_click:
            on_click()
        
        return clicked
    
    @staticmethod
    def primary(
        label: str,
        key: Optional[str] = None,
        icon: Optional[str] = None,
        **kwargs
    ) -> bool:
        """Botón primario (acción principal)"""
        return UIButton.render(label, key, variant="primary", icon=icon, **kwargs)
    
    @staticmethod
    def secondary(
        label: str,
        key: Optional[str] = None,
        icon: Optional[str] = None,
        **kwargs
    ) -> bool:
        """Botón secundario (acción alternativa)"""
        return UIButton.render(label, key, variant="secondary", icon=icon, **kwargs)
    
    @staticmethod
    def success(
        label: str,
        key: Optional[str] = None,
        icon: str = "✓",
        **kwargs
    ) -> bool:
        """Botón de éxito (acciones positivas)"""
        return UIButton.render(label, key, variant="success", icon=icon, **kwargs)
    
    @staticmethod
    def danger(
        label: str,
        key: Optional[str] = None,
        icon: str = "⚠️",
        **kwargs
    ) -> bool:
        """Botón de peligro (acciones destructivas)"""
        return UIButton.render(label, key, variant="danger", icon=icon, **kwargs)
    
    @staticmethod
    def warning(
        label: str,
        key: Optional[str] = None,
        icon: str = "⚡",
        **kwargs
    ) -> bool:
        """Botón de advertencia (acciones que requieren atención)"""
        return UIButton.render(label, key, variant="warning", icon=icon, **kwargs)
    
    @staticmethod
    def outline(
        label: str,
        key: Optional[str] = None,
        icon: Optional[str] = None,
        **kwargs
    ) -> bool:
        """Botón outline (menor énfasis)"""
        return UIButton.render(label, key, variant="outline", icon=icon, **kwargs)


class ActionButtons:
    """Botones de acción específicos para el flujo de triaje"""
    
    @staticmethod
    def call_button(
        patient_id: str,
        on_click: Optional[Callable] = None,
        key: Optional[str] = None
    ) -> bool:
        """Botón para llamar paciente"""
        return UIButton.success(
            "Llamar",
            key=key or f"call_{patient_id}",
            icon="📞",
            on_click=on_click
        )
    
    @staticmethod
    def view_button(
        patient_id: str,
        on_click: Optional[Callable] = None,
        key: Optional[str] = None
    ) -> bool:
        """Botón para ver detalles"""
        return UIButton.secondary(
            "Ver",
            key=key or f"view_{patient_id}",
            icon="👁️",
            on_click=on_click
        )
    
    @staticmethod
    def return_button(
        patient_id: str,
        on_click: Optional[Callable] = None,
        key: Optional[str] = None
    ) -> bool:
        """Botón para devolver paciente"""
        return UIButton.warning(
            "Devolver",
            key=key or f"return_{patient_id}",
            icon="↩️",
            on_click=on_click
        )
    
    @staticmethod
    def attend_button(
        patient_id: str,
        on_click: Optional[Callable] = None,
        key: Optional[str] = None
    ) -> bool:
        """Botón para atender paciente"""
        return UIButton.primary(
            "Atender",
            key=key or f"attend_{patient_id}",
            icon="🏥",
            on_click=on_click
        )
    
    @staticmethod
    def save_button(
        on_click: Optional[Callable] = None,
        key: Optional[str] = None,
        full_width: bool = False
    ) -> bool:
        """Botón para guardar"""
        return UIButton.success(
            "Guardar",
            key=key or "save_btn",
            icon="💾",
            on_click=on_click,
            full_width=full_width
        )
    
    @staticmethod
    def cancel_button(
        on_click: Optional[Callable] = None,
        key: Optional[str] = None,
        full_width: bool = False
    ) -> bool:
        """Botón para cancelar"""
        return UIButton.outline(
            "Cancelar",
            key=key or "cancel_btn",
            icon="✕",
            on_click=on_click,
            full_width=full_width
        )
    
    @staticmethod
    def delete_button(
        on_click: Optional[Callable] = None,
        key: Optional[str] = None,
        confirm: bool = True
    ) -> bool:
        """Botón para eliminar (con confirmación opcional)"""
        return UIButton.danger(
            "Eliminar",
            key=key or "delete_btn",
            icon="🗑️",
            on_click=on_click
        )
    
    @staticmethod
    def edit_button(
        on_click: Optional[Callable] = None,
        key: Optional[str] = None
    ) -> bool:
        """Botón para editar"""
        return UIButton.secondary(
            "Editar",
            key=key or "edit_btn",
            icon="✏️",
            on_click=on_click
        )
    
    @staticmethod
    def next_button(
        on_click: Optional[Callable] = None,
        key: Optional[str] = None,
        full_width: bool = False
    ) -> bool:
        """Botón para siguiente paso"""
        return UIButton.primary(
            "Siguiente",
            key=key or "next_btn",
            icon="→",
            on_click=on_click,
            full_width=full_width
        )
    
    @staticmethod
    def back_button(
        on_click: Optional[Callable] = None,
        key: Optional[str] = None,
        full_width: bool = False
    ) -> bool:
        """Botón para paso anterior"""
        return UIButton.outline(
            "Atrás",
            key=key or "back_btn",
            icon="←",
            on_click=on_click,
            full_width=full_width
        )
    
    @staticmethod
    def finish_button(
        on_click: Optional[Callable] = None,
        key: Optional[str] = None,
        full_width: bool = False
    ) -> bool:
        """Botón para finalizar"""
        return UIButton.success(
            "Finalizar",
            key=key or "finish_btn",
            icon="✓",
            on_click=on_click,
            full_width=full_width
        )
    
    @staticmethod
    def search_button(
        on_click: Optional[Callable] = None,
        key: Optional[str] = None
    ) -> bool:
        """Botón para buscar"""
        return UIButton.primary(
            "Buscar",
            key=key or "search_btn",
            icon="🔍",
            on_click=on_click
        )
    
    @staticmethod
    def refresh_button(
        on_click: Optional[Callable] = None,
        key: Optional[str] = None
    ) -> bool:
        """Botón para refrescar"""
        return UIButton.secondary(
            "Refrescar",
            key=key or "refresh_btn",
            icon="🔄",
            on_click=on_click
        )
    
    @staticmethod
    def export_button(
        on_click: Optional[Callable] = None,
        key: Optional[str] = None
    ) -> bool:
        """Botón para exportar"""
        return UIButton.outline(
            "Exportar",
            key=key or "export_btn",
            icon="📥",
            on_click=on_click
        )
    
    @staticmethod
    def print_button(
        on_click: Optional[Callable] = None,
        key: Optional[str] = None
    ) -> bool:
        """Botón para imprimir"""
        return UIButton.outline(
            "Imprimir",
            key=key or "print_btn",
            icon="🖨️",
            on_click=on_click
        )


class ButtonGroup:
    """Grupos de botones relacionados"""
    
    @staticmethod
    def save_cancel(
        on_save: Optional[Callable] = None,
        on_cancel: Optional[Callable] = None,
        key_prefix: str = "sc"
    ) -> tuple:
        """Grupo Guardar/Cancelar"""
        col1, col2 = st.columns(2)
        
        with col1:
            save_clicked = UIButton.success(
                "Guardar",
                key=f"{key_prefix}_save",
                icon="💾",
                on_click=on_save,
                full_width=True
            )
        
        with col2:
            cancel_clicked = UIButton.outline(
                "Cancelar",
                key=f"{key_prefix}_cancel",
                icon="✕",
                on_click=on_cancel,
                full_width=True
            )
        
        return save_clicked, cancel_clicked
    
    @staticmethod
    def next_back(
        on_next: Optional[Callable] = None,
        on_back: Optional[Callable] = None,
        key_prefix: str = "nb",
        show_back: bool = True
    ) -> tuple:
        """Grupo Siguiente/Atrás para wizards"""
        if show_back:
            col1, col2 = st.columns([1, 1])
            with col1:
                back_clicked = UIButton.outline(
                    "Atrás",
                    key=f"{key_prefix}_back",
                    icon="←",
                    on_click=on_back,
                    full_width=True
                )
            with col2:
                next_clicked = UIButton.primary(
                    "Siguiente",
                    key=f"{key_prefix}_next",
                    icon="→",
                    on_click=on_next,
                    full_width=True
                )
            return next_clicked, back_clicked
        else:
            next_clicked = UIButton.primary(
                "Siguiente",
                key=f"{key_prefix}_next",
                icon="→",
                on_click=on_next,
                full_width=True
            )
            return next_clicked, False
    
    @staticmethod
    def finish_cancel(
        on_finish: Optional[Callable] = None,
        on_cancel: Optional[Callable] = None,
        key_prefix: str = "fc"
    ) -> tuple:
        """Grupo Finalizar/Cancelar"""
        col1, col2 = st.columns(2)
        
        with col1:
            finish_clicked = UIButton.success(
                "Finalizar",
                key=f"{key_prefix}_finish",
                icon="✓",
                on_click=on_finish,
                full_width=True
            )
        
        with col2:
            cancel_clicked = UIButton.outline(
                "Cancelar",
                key=f"{key_prefix}_cancel",
                icon="✕",
                on_click=on_cancel,
                full_width=True
            )
        
        return finish_clicked, cancel_clicked
    
    @staticmethod
    def confirm_delete(
        on_confirm: Optional[Callable] = None,
        on_cancel: Optional[Callable] = None,
        key_prefix: str = "cd"
    ) -> tuple:
        """Grupo Confirmar eliminación/Cancelar"""
        col1, col2 = st.columns(2)
        
        with col1:
            confirm_clicked = UIButton.danger(
                "Eliminar",
                key=f"{key_prefix}_confirm",
                icon="🗑️",
                on_click=on_confirm,
                full_width=True
            )
        
        with col2:
            cancel_clicked = UIButton.outline(
                "Cancelar",
                key=f"{key_prefix}_cancel",
                icon="✕",
                on_click=on_cancel,
                full_width=True
            )
        
        return confirm_clicked, cancel_clicked
    
    @staticmethod
    def patient_actions(
        patient_id: str,
        on_call: Optional[Callable] = None,
        on_view: Optional[Callable] = None,
        on_return: Optional[Callable] = None
    ) -> dict:
        """Grupo de acciones de paciente (Llamar/Ver/Devolver)"""
        col1, col2, col3 = st.columns(3)
        
        actions = {}
        
        with col1:
            actions['call'] = ActionButtons.call_button(patient_id, on_call)
        
        with col2:
            actions['view'] = ActionButtons.view_button(patient_id, on_view)
        
        with col3:
            actions['return'] = ActionButtons.return_button(patient_id, on_return)
        
        return actions


# Helper functions para uso directo
def btn_primary(label: str, **kwargs) -> bool:
    """Helper para botón primario"""
    return UIButton.primary(label, **kwargs)

def btn_secondary(label: str, **kwargs) -> bool:
    """Helper para botón secundario"""
    return UIButton.secondary(label, **kwargs)

def btn_success(label: str, **kwargs) -> bool:
    """Helper para botón de éxito"""
    return UIButton.success(label, **kwargs)

def btn_danger(label: str, **kwargs) -> bool:
    """Helper para botón de peligro"""
    return UIButton.danger(label, **kwargs)

def btn_warning(label: str, **kwargs) -> bool:
    """Helper para botón de advertencia"""
    return UIButton.warning(label, **kwargs)

def btn_outline(label: str, **kwargs) -> bool:
    """Helper para botón outline"""
    return UIButton.outline(label, **kwargs)

def btn_call(patient_id: str, **kwargs) -> bool:
    """Helper para botón llamar"""
    return ActionButtons.call_button(patient_id, **kwargs)

def btn_view(patient_id: str, **kwargs) -> bool:
    """Helper para botón ver"""
    return ActionButtons.view_button(patient_id, **kwargs)

def btn_return(patient_id: str, **kwargs) -> bool:
    """Helper para botón devolver"""
    return ActionButtons.return_button(patient_id, **kwargs)

def btn_save(**kwargs) -> bool:
    """Helper para botón guardar"""
    return ActionButtons.save_button(**kwargs)

def btn_cancel(**kwargs) -> bool:
    """Helper para botón cancelar"""
    return ActionButtons.cancel_button(**kwargs)

def btn_next(**kwargs) -> bool:
    """Helper para botón siguiente"""
    return ActionButtons.next_button(**kwargs)

def btn_back(**kwargs) -> bool:
    """Helper para botón atrás"""
    return ActionButtons.back_button(**kwargs)

def btn_finish(**kwargs) -> bool:
    """Helper para botón finalizar"""
    return ActionButtons.finish_button(**kwargs)
