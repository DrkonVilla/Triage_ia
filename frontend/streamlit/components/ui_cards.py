"""
Componentes de UI reutilizables para el Sistema de Triaje Clínico
Tarjetas, KPIs y contenedores de sección modernos
"""

import streamlit as st
from typing import Optional, List, Dict, Any, Callable


class UICard:
    """Sistema de tarjetas estilizadas con soporte para diferentes layouts"""
    
    @staticmethod
    def patient_card(
        patient_id: str,
        name: str,
        urgency_level: str,  # RED, ORANGE, YELLOW, GREEN, BLUE
        age: int,
        motive: str,
        wait_time: str,
        on_call: Optional[Callable] = None,
        on_view: Optional[Callable] = None,
        on_return: Optional[Callable] = None,
        is_selected: bool = False,
        is_critical: bool = False
    ) -> None:
        """
        Renderiza una tarjeta de paciente para el Kanban
        
        Args:
            patient_id: ID del paciente
            name: Nombre completo
            urgency_level: Nivel de urgencia (RED, ORANGE, YELLOW, GREEN, BLUE)
            age: Edad del paciente
            motive: Motivo de consulta
            wait_time: Tiempo de espera
            on_call: Callback para "Llamar"
            on_view: Callback para "Ver"
            on_return: Callback para "Devolver"
            is_selected: Si la tarjeta está seleccionada
            is_critical: Si es caso crítico (animación pulse)
        """
        urgency_class = f"urgency-{urgency_level.lower()}"
        selected_class = "selected" if is_selected else ""
        critical_class = "critical" if is_critical else ""
        
        # Mapeo de colores a emojis
        urgency_emojis = {
            "RED": "🔴",
            "ORANGE": "🟠", 
            "YELLOW": "🟡",
            "GREEN": "🟢",
            "BLUE": "🔵"
        }
        
        urgency_labels = {
            "RED": "CRÍTICO",
            "ORANGE": "URGENCIA",
            "YELLOW": "POCO URGENTE",
            "GREEN": "NO URGENTE",
            "BLUE": "ADMINISTRATIVO"
        }
        
        html = f"""
        <div class="patient-card {urgency_class} {selected_class} {critical_class}">
            <div class="patient-card-header">
                <div>
                    <p class="patient-name">{name}</p>
                    <p class="patient-id">ID: {patient_id} • {age} años</p>
                </div>
                <span class="urgency-badge {urgency_class}">
                    {urgency_emojis.get(urgency_level, "⚪")} {urgency_labels.get(urgency_level, urgency_level)}
                </span>
            </div>
            <div class="patient-details">
                <span>⏱️ {wait_time}</span>
            </div>
            <div class="patient-motive">
                📝 {motive}
            </div>
        </div>
        """
        st.markdown(html, unsafe_allow_html=True)
        
        # Botones de acción
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if on_call and st.button("📞 Llamar", key=f"call_{patient_id}", type="primary"):
                on_call(patient_id)
        
        with col2:
            if on_view and st.button("👁️ Ver", key=f"view_{patient_id}"):
                on_view(patient_id)
        
        with col3:
            if on_return and st.button("↩️ Devolver", key=f"return_{patient_id}"):
                on_return(patient_id)

    @staticmethod
    def section_card(
        title: str,
        step_number: Optional[int] = None,
        content_func: Optional[Callable] = None
    ) -> None:
        """
        Renderiza una sección en formato card con header estilizado
        
        Args:
            title: Título de la sección
            step_number: Número de paso (opcional, para wizard)
            content_func: Función que renderiza el contenido interno
        """
        step_html = f"""
            <div class="section-number">{step_number}</div>
        """ if step_number else ""
        
        html = f"""
        <div class="section-card">
            <div class="section-header">
                {step_html}
                <h3 class="section-title">{title}</h3>
            </div>
        """
        st.markdown(html, unsafe_allow_html=True)
        
        if content_func:
            content_func()
        
        st.markdown("</div>", unsafe_allow_html=True)


class KPICard:
    """Componentes de métricas KPI estilizadas"""
    
    @staticmethod
    def render(
        label: str,
        value: str,
        icon: str = "📊",
        delta: Optional[str] = None,
        delta_positive: bool = True,
        variant: str = "primary"  # primary, success, warning, danger
    ) -> None:
        """
        Renderiza una tarjeta KPI con icono y delta opcional
        
        Args:
            label: Etiqueta de la métrica
            value: Valor principal
            icon: Emoji/icono
            delta: Texto de cambio (ej: "+12% vs mes anterior")
            delta_positive: Si el cambio es positivo (afecta color)
            variant: Variante de color (primary, success, warning, danger)
        """
        delta_html = ""
        if delta:
            delta_class = "positive" if delta_positive else "negative"
            delta_icon = "📈" if delta_positive else "📉"
            delta_html = f"""
                <div class="kpi-delta {delta_class}">
                    {delta_icon} {delta}
                </div>
            """
        
        html = f"""
        <div class="kpi-card">
            <div class="kpi-header">
                <div class="kpi-icon {variant}">
                    {icon}
                </div>
            </div>
            <p class="kpi-label">{label}</p>
            <p class="kpi-value">{value}</p>
            {delta_html}
        </div>
        """
        st.markdown(html, unsafe_allow_html=True)
    
    @staticmethod
    def grid(kpis: List[Dict[str, Any]], columns: int = 4) -> None:
        """
        Renderiza una grid de KPIs
        
        Args:
            kpis: Lista de diccionarios con keys: label, value, icon, delta, delta_positive, variant
            columns: Número de columnas (2-4)
        """
        cols = st.columns(columns)
        
        for idx, kpi in enumerate(kpis):
            with cols[idx % columns]:
                KPICard.render(
                    label=kpi.get("label", ""),
                    value=kpi.get("value", ""),
                    icon=kpi.get("icon", "📊"),
                    delta=kpi.get("delta"),
                    delta_positive=kpi.get("delta_positive", True),
                    variant=kpi.get("variant", "primary")
                )


class EmptyState:
    """Estado vacío con mensaje e icono"""
    
    @staticmethod
    def render(
        message: str = "No hay datos disponibles",
        icon: str = "📭",
        submessage: Optional[str] = None
    ) -> None:
        """
        Renderiza un estado vacío
        
        Args:
            message: Mensaje principal
            icon: Emoji principal
            submessage: Mensaje secundario opcional
        """
        sub_html = f"""
            <p style="font-size: 14px; margin-top: 8px;">{submessage}</p>
        """ if submessage else ""
        
        html = f"""
        <div class="empty-state">
            <div class="empty-state-icon">{icon}</div>
            <p style="font-size: 16px; font-weight: 500;">{message}</p>
            {sub_html}
        </div>
        """
        st.markdown(html, unsafe_allow_html=True)


class WizardSteps:
    """Indicador de pasos tipo wizard"""
    
    @staticmethod
    def render(
        steps: List[str],
        current_step: int,
        completed_steps: Optional[List[int]] = None
    ) -> None:
        """
        Renderiza un wizard de pasos
        
        Args:
            steps: Lista de nombres de pasos
            current_step: Índice del paso actual (0-based)
            completed_steps: Lista de índices de pasos completados
        """
        if completed_steps is None:
            completed_steps = list(range(current_step))
        
        steps_html = []
        for idx, step_name in enumerate(steps):
            if idx in completed_steps:
                step_class = "completed"
                icon = "✓"
            elif idx == current_step:
                step_class = "active"
                icon = str(idx + 1)
            else:
                step_class = ""
                icon = str(idx + 1)
            
            steps_html.append(f"""
                <div class="wizard-step {step_class}">
                    <span>{icon}</span>
                    <span>{step_name}</span>
                </div>
            """)
        
        # Añadir conectores
        final_html = []
        for i, step_html in enumerate(steps_html):
            final_html.append(step_html)
            if i < len(steps_html) - 1:
                final_html.append('<div class="wizard-connector"></div>')
        
        html = f"""
        <div class="wizard-steps">
            {''.join(final_html)}
        </div>
        """
        st.markdown(html, unsafe_allow_html=True)


class Chip:
    """Componente Chip/Tag seleccionable"""
    
    @staticmethod
    def render(
        label: str,
        selected: bool = False,
        key: Optional[str] = None
    ) -> bool:
        """
        Renderiza un chip seleccionable
        
        Args:
            label: Texto del chip
            selected: Estado inicial
            key: Key única para el botón
            
        Returns:
            True si está seleccionado después del click
        """
        chip_class = "selected" if selected else ""
        
        # Usar st.button para interactividad
        clicked = st.button(
            label,
            key=key or f"chip_{label}",
            type="primary" if selected else "secondary"
        )
        
        return not selected if clicked else selected
    
    @staticmethod
    def group(
        options: List[str],
        selected: Optional[List[str]] = None,
        multi_select: bool = True,
        key_prefix: str = "chip_group"
    ) -> List[str]:
        """
        Renderiza un grupo de chips
        
        Args:
            options: Lista de opciones
            selected: Opciones inicialmente seleccionadas
            multi_select: Permitir selección múltiple
            key_prefix: Prefijo para las keys
            
        Returns:
            Lista de opciones seleccionadas
        """
        if selected is None:
            selected = []
        
        current_selected = selected.copy()
        
        cols = st.columns(len(options))
        for idx, option in enumerate(options):
            with cols[idx]:
                is_selected = option in current_selected
                if st.button(
                    option,
                    key=f"{key_prefix}_{idx}",
                    type="primary" if is_selected else "secondary"
                ):
                    if multi_select:
                        if is_selected:
                            current_selected.remove(option)
                        else:
                            current_selected.append(option)
                    else:
                        current_selected = [option] if not is_selected else []
        
        return current_selected


class LoginCard:
    """Tarjeta de login estilizada"""
    
    @staticmethod
    def render_header(
        title: str = "Sistema de Triaje",
        subtitle: str = "Inicie sesión para continuar",
        logo_emoji: str = "🏥"
    ) -> None:
        """Renderiza el header de la tarjeta de login"""
        html = f"""
        <div class="login-logo">
            <div class="login-logo-icon">{logo_emoji}</div>
        </div>
        <h1 class="login-title">{title}</h1>
        <p class="login-subtitle">{subtitle}</p>
        """
        st.markdown(html, unsafe_allow_html=True)
    
    @staticmethod
    def render_footer(text: str = "© 2024 Hospital Clínico. Todos los derechos reservados.") -> None:
        """Renderiza el footer de la tarjeta de login"""
        html = f"""
        <p class="login-footer">{text}</p>
        """
        st.markdown(html, unsafe_allow_html=True)


class UrgencyBadge:
    """Badge de urgencia con color y emoji"""
    
    LEVELS = {
        "RED": {"emoji": "🔴", "label": "CRÍTICO", "class": "urgency-red"},
        "ORANGE": {"emoji": "🟠", "label": "URGENCIA", "class": "urgency-orange"},
        "YELLOW": {"emoji": "🟡", "label": "POCO URGENTE", "class": "urgency-yellow"},
        "GREEN": {"emoji": "🟢", "label": "NO URGENTE", "class": "urgency-green"},
        "BLUE": {"emoji": "🔵", "label": "ADMINISTRATIVO", "class": "urgency-blue"}
    }
    
    @classmethod
    def render(cls, level: str, show_emoji: bool = True) -> None:
        """
        Renderiza un badge de urgencia
        
        Args:
            level: Nivel de urgencia (RED, ORANGE, YELLOW, GREEN, BLUE)
            show_emoji: Mostrar emoji junto al texto
        """
        config = cls.LEVELS.get(level.upper(), cls.LEVELS["BLUE"])
        
        content = f"{config['emoji']} {config['label']}" if show_emoji else config['label']
        
        html = f"""
        <span class="urgency-badge {config['class']}">
            {content}
        </span>
        """
        st.markdown(html, unsafe_allow_html=True)
    
    @classmethod
    def get_color(cls, level: str) -> str:
        """Retorna el color CSS para un nivel de urgencia"""
        colors = {
            "RED": "#DC2626",
            "ORANGE": "#EA580C",
            "YELLOW": "#D97706",
            "GREEN": "#059669",
            "BLUE": "#2563EB"
        }
        return colors.get(level.upper(), "#9CA3AF")
    
    @classmethod
    def get_bg_color(cls, level: str) -> str:
        """Retorna el color de fondo para un nivel de urgencia"""
        colors = {
            "RED": "#FEE2E2",
            "ORANGE": "#FFEDD5",
            "YELLOW": "#FEF3C7",
            "GREEN": "#D1FAE5",
            "BLUE": "#DBEAFE"
        }
        return colors.get(level.upper(), "#F3F4F6")


# Helper functions para uso directo
def render_patient_card(*args, **kwargs):
    """Helper para renderizar tarjeta de paciente"""
    UICard.patient_card(*args, **kwargs)

def render_kpi(label: str, value: str, **kwargs):
    """Helper para renderizar KPI"""
    KPICard.render(label, value, **kwargs)

def render_kpi_grid(kpis: List[Dict[str, Any]], columns: int = 4):
    """Helper para renderizar grid de KPIs"""
    KPICard.grid(kpis, columns)

def render_empty_state(message: str = "No hay datos disponibles", **kwargs):
    """Helper para renderizar estado vacío"""
    EmptyState.render(message, **kwargs)

def render_wizard_steps(steps: List[str], current_step: int, **kwargs):
    """Helper para renderizar wizard"""
    WizardSteps.render(steps, current_step, **kwargs)

def render_section_card(title: str, step_number: Optional[int] = None, content_func=None):
    """Helper para renderizar sección"""
    UICard.section_card(title, step_number, content_func)

def render_urgency_badge(level: str, show_emoji: bool = True):
    """Helper para renderizar badge de urgencia"""
    UrgencyBadge.render(level, show_emoji)
