import streamlit as st

def display_kpi_metrics(en_espera: int, delta_espera: int, tiempo_promedio: float, 
                        tiempo_anterior: float, criticos: int):
    """Muestra tarjetas de KPIs en el dashboard"""
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        delta_color = "inverse" if delta_espera > 0 else "normal"
        st.metric(
            "⏳ Triajes en Espera", 
            en_espera, 
            delta=f"{delta_espera:+d} vs turno anterior",
            delta_color=delta_color
        )
    
    with col2:
        delta_tiempo = tiempo_promedio - tiempo_anterior
        st.metric(
            "⏱️ Promedio Tiempo Triaje", 
            f"{tiempo_promedio:.1f} min",
            delta=f"{delta_tiempo:+.1f} min",
            delta_color="inverse" if delta_tiempo > 0 else "normal"
        )
    
    with col3:
        st.metric(
            "🔴 Pacientes Rojo/Naranja", 
            criticos,
            delta="⚠️ Prioridad máxima" if criticos > 0 else None
        )

def display_alert_banner(has_criticos: bool):
    """Muestra banner de alerta si hay pacientes críticos"""
    
    if has_criticos:
        st.warning("""
        ⚠️ **ALERTA DE SEGURIDAD** ⚠️  
        Hay pacientes con nivel de urgencia ROJO o NARANJA en espera.  
        Priorice su atención inmediata.
        """)