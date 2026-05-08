import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from utils import *
import sys
import os
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")
# Agregar parent al path para importar auth_persistence
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from components.auth_persistence import verify_and_restore_session

st.set_page_config(page_title="Dashboard Operativo", page_icon="📊", layout="wide")

# Intentar restaurar sesión si no está autenticado


if not st.session_state.get('authenticated'):
    if verify_and_restore_session(API_BASE_URL):
        st.rerun()

# Verificar autenticación
if 'authenticated' not in st.session_state:
    st.error("Por favor inicie sesión")
    st.stop()

# Header moderno
st.markdown("""
<h1 style="font-size: 28px; font-weight: 700; color: #0D47A1; margin-bottom: 8px;">
    📊 Dashboard Operativo
</h1>
<p style="color: #616161; margin-bottom: 24px;">
    Unidad de Triaje - Métricas y KPIs en tiempo real
</p>
""", unsafe_allow_html=True)

# --- SELECTOR DE RANGO DE FECHAS ---
col_selector, col_refresh = st.columns([3, 1])

with col_selector:
    st.markdown("**📅 Período de visualización:**")
    rango_options = {
        "hoy": "📅 Hoy",
        "mes": "📆 Este Mes",
        "total": "📊 Histórico Total"
    }
    rango_seleccionado = st.radio(
        "Seleccione el período:",
        options=["hoy", "mes", "total"],
        format_func=lambda x: rango_options[x],
        horizontal=True,
        label_visibility="collapsed"
    )

with col_refresh:
    st.markdown("####")
    if st.button("🔄 Actualizar", use_container_width=True):
        st.cache_data.clear()
        st.rerun()

st.markdown("---")

# --- CARGAR DATOS REALES DEL BACKEND ---
@st.cache_data(ttl=30)  # Cachear 30 segundos
def cargar_dashboard(rango: str):
    return obtener_dashboard_operativo(rango)

with st.spinner(f"🔄 Cargando datos ({rango_seleccionado})..."):
    data = cargar_dashboard(rango_seleccionado)

if not data:
    st.error("❌ No se pudieron cargar los datos del dashboard. Verifique la conexión con el backend.")
    st.stop()

kpis = data.get('kpis', {})
top_sintomas = data.get('top_sintomas', [])
flujo_por_hora = data.get('flujo_por_hora', [])
distribucion = data.get('distribucion_urgencia', [])
resumen = data.get('resumen_turno', {})

actualizado = data.get('actualizado', datetime.now().isoformat())
rango_titulo = data.get('rango', 'Hoy')
st.caption(f"🕐 Última actualización: {actualizado[:19]} | 📅 Período: **{rango_titulo}**")

st.markdown("---")

# --- KPIs con diseño moderno ---
st.markdown(f"""
<div style="font-size: 18px; font-weight: 600; color: #212121; margin-bottom: 16px;">
    🎯 Indicadores Clave - {rango_titulo}
</div>
""", unsafe_allow_html=True)

# Función para renderizar KPI card
def render_kpi_card(label, value, icon, color, delta=None):
    delta_html = ""
    if delta:
        delta_color = "#43A047" if delta > 0 else "#E53935"
        delta_icon = "📈" if delta > 0 else "📉"
        delta_html = f'<div style="font-size: 12px; color: {delta_color}; margin-top: 8px;">{delta_icon} {abs(delta)}%</div>'
    
    return f"""
    <div style="background: white; border-radius: 12px; padding: 20px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); border: 1px solid #EEEEEE;">
        <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 12px;">
            <div style="width: 48px; height: 48px; border-radius: 8px; background: {color}20; display: flex; align-items: center; justify-content: center; font-size: 24px;">
                {icon}
            </div>
        </div>
        <div style="font-size: 14px; color: #616161; font-weight: 500;">{label}</div>
        <div style="font-size: 32px; font-weight: 700; color: #212121; margin-top: 4px;">{value}</div>
        {delta_html}
    </div>
    """

col1, col2, col3, col4 = st.columns(4)

with col1:
    en_espera = kpis.get('en_espera', 0)
    st.markdown(render_kpi_card("En Espera", en_espera, "⏳", "#1E88E5"), unsafe_allow_html=True)

with col2:
    tiempo_promedio = kpis.get('tiempo_promedio_min', 0)
    st.markdown(render_kpi_card("Tiempo Promedio", f"{tiempo_promedio} min", "⏱️", "#00ACC1"), unsafe_allow_html=True)

with col3:
    criticos = kpis.get('criticos', 0)
    criticos_color = "#E53935" if criticos > 0 else "#9E9E9E"
    st.markdown(render_kpi_card("Casos Críticos", criticos, "🔴", criticos_color), unsafe_allow_html=True)

with col4:
    total = kpis.get('total_triajes', 0) or resumen.get('total_atendidos', 0)
    st.markdown(render_kpi_card("Total Atendidos", total, "🏥", "#43A047"), unsafe_allow_html=True)

st.markdown("---")

# --- GRÁFICO 1: Barras Horizontales - Top Síntomas ---
st.markdown("""
<div style="background: white; border-radius: 12px; padding: 24px; margin-top: 24px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); border: 1px solid #EEEEEE;">
    <div style="font-size: 18px; font-weight: 600; color: #212121; margin-bottom: 16px;">
        📈 Top Síntomas Reportados
    </div>
""", unsafe_allow_html=True)

# Usar datos reales del backend
if top_sintomas:
    sintomas_data = {
        'Síntoma': [s['sintoma'] for s in top_sintomas],
        'Frecuencia': [s['frecuencia'] for s in top_sintomas]
    }
else:
    sintomas_data = {'Síntoma': ['Sin datos'], 'Frecuencia': [0]}

df_sintomas = pd.DataFrame(sintomas_data)

fig_bar = px.bar(df_sintomas, 
                  x='Frecuencia', 
                  y='Síntoma', 
                  orientation='h',
                  title=f'Frecuencia de Síntomas - {rango_titulo}',
                  color='Frecuencia',
                  color_continuous_scale='Reds',
                  text='Frecuencia')
fig_bar.update_layout(height=400, xaxis_title="Número de casos", yaxis_title="")
st.plotly_chart(fig_bar, use_container_width=True)

st.markdown("</div>", unsafe_allow_html=True)

# --- GRÁFICO 2: Time Series - Flujo de Llegadas ---
st.markdown("""
<div style="background: white; border-radius: 12px; padding: 24px; margin-top: 24px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); border: 1px solid #EEEEEE;">
    <div style="font-size: 18px; font-weight: 600; color: #212121; margin-bottom: 16px;">
        📅 Flujo de Pacientes
    </div>
""", unsafe_allow_html=True)

if rango_seleccionado == "hoy":
    eje_x_label = "Hora del día"
    titulo_flujo = "Flujo de Llegadas por Hora"
elif rango_seleccionado == "mes":
    eje_x_label = "Día del mes"
    titulo_flujo = "Flujo de Llegadas por Día"
else:
    eje_x_label = "Mes"
    titulo_flujo = "Flujo de Llegadas por Mes"

# Usar datos reales del backend
if flujo_por_hora:
    horas = [f['hora'] for f in flujo_por_hora]
    llegadas = [f['llegadas'] for f in flujo_por_hora]
else:
    horas = list(range(24))
    llegadas = [0] * 24

df_flujo = pd.DataFrame({'Hora': horas, 'Llegadas': llegadas})

fig_line = px.line(df_flujo, 
                    x='Hora', 
                    y='Llegadas',
                    title=titulo_flujo,
                    markers=True,
                    labels={'Hora': eje_x_label, 'Llegadas': 'Número de pacientes'})
fig_line.update_traces(line=dict(color='#2E86C1', width=3), marker=dict(size=8))
fig_line.add_hline(y=df_flujo['Llegadas'].mean(), line_dash="dash", line_color="red", 
                   annotation_text=f"Promedio: {df_flujo['Llegadas'].mean():.1f}")
st.plotly_chart(fig_line, use_container_width=True)

st.markdown("</div>", unsafe_allow_html=True)

# --- GRÁFICO 3: Pie - Distribución por Nivel de Urgencia ---
st.markdown("""
<div style="background: white; border-radius: 12px; padding: 24px; margin-top: 24px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); border: 1px solid #EEEEEE;">
    <div style="font-size: 18px; font-weight: 600; color: #212121; margin-bottom: 16px;">
        🥧 Distribución por Nivel de Urgencia
    </div>
""", unsafe_allow_html=True)

# Usar datos reales del backend
niveles_labels = {
    'RED': 'RED (Crítico)',
    'ORANGE': 'ORANGE (Urgente)',
    'YELLOW': 'YELLOW (Poco Urgente)',
    'GREEN': 'GREEN (No Urgente)',
    'BLUE': 'BLUE (Admin)'
}

if distribucion:
    niveles = [niveles_labels.get(d['nivel'], d['nivel']) for d in distribucion]
    cantidades = [d['cantidad'] for d in distribucion]
else:
    niveles = list(niveles_labels.values())
    cantidades = [0, 0, 0, 0, 0]

colores = ['#FF0000', '#FFA500', '#FFFF00', '#00FF00', '#0000FF']

fig_pie = go.Figure(data=[go.Pie(labels=niveles, 
                                 values=cantidades, 
                                 hole=0.3,
                                 marker_colors=colores,
                                 textinfo='label+percent',
                                 textposition='auto')])
fig_pie.update_layout(height=400, showlegend=True, legend=dict(orientation="h", yanchor="bottom", y=-0.2))
st.plotly_chart(fig_pie, use_container_width=True)
st.markdown("</div>", unsafe_allow_html=True)

# --- Tabla de Resumen de Turno ---
st.markdown("""
<div style="background: white; border-radius: 12px; padding: 24px; margin-top: 24px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); border: 1px solid #EEEEEE;">
    <div style="font-size: 18px; font-weight: 600; color: #212121; margin-bottom: 16px;">
        📋 Resumen del Período
    </div>
""", unsafe_allow_html=True)

# Usar datos reales del backend
if resumen:
    resumen_data = {
        'Total Pacientes Atendidos': [resumen.get('total_atendidos', 0)],
        'Tiempo Promedio Atención': [f"{kpis.get('tiempo_promedio_min', 0)} min"],
        'Tasa Confirmación IA': [f"{resumen.get('tasa_confirmacion', 0)}%"],
        'Sugerencias IA Confirmadas': [resumen.get('confirmados_ia', 0)],
        'Discrepancias IA/Enfermera': [resumen.get('discrepancias', 0)]
    }
else:
    resumen_data = {
        'Total Pacientes Atendidos': [0],
        'Tiempo Promedio Atención': ['0 min'],
        'Tasa Confirmación IA': ['0%'],
        'Sugerencias IA Confirmadas': [0],
        'Discrepancias IA/Enfermera': [0]
    }

# Mostrar información adicional según el rango
total_triajes = resumen.get('total_atendidos', 0) if resumen else 0
st.info(f"📊 Mostrando datos de: **{rango_titulo}** | Total de triajes en período: **{total_triajes}**")

df_resumen = pd.DataFrame(resumen_data)
st.dataframe(df_resumen, use_container_width=True, hide_index=True)

st.markdown("</div>", unsafe_allow_html=True)

# --- Exportar Reporte PDF ---
st.markdown("""
<div style="background: white; border-radius: 12px; padding: 24px; margin-top: 24px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); border: 1px solid #EEEEEE;">
    <div style="font-size: 18px; font-weight: 600; color: #212121; margin-bottom: 16px;">
        📄 Exportar Reporte
    </div>
""", unsafe_allow_html=True)

col_export, col_empty = st.columns([1, 3])
with col_export:
    pdf_label = {"hoy": "de Hoy", "mes": "del Mes", "total": "Histórico"}
    if st.button(f"📄 Exportar Reporte {pdf_label.get(rango_seleccionado, '')} (PDF)", type="primary", use_container_width=True):
        headers = get_auth_headers()
        try:
            with st.spinner(f"📄 Generando reporte {pdf_label.get(rango_seleccionado, '')}..."):
                response = requests.get(
                    f"{API_BASE_URL}/api/v1/reportes/shift-pdf",
                    headers=headers,
                    params={"rango": rango_seleccionado},
                    timeout=30
                )
                if response.status_code == 200:
                    # Ofrecer descarga
                    pdf_bytes = response.content
                    filename = f"reporte_turno_{rango_seleccionado}_{datetime.now().strftime('%Y%m%d')}.pdf"
                    st.download_button(
                        label="⬇️ Descargar Reporte PDF",
                        data=pdf_bytes,
                        file_name=filename,
                        mime="application/pdf",
                        use_container_width=True
                    )
                    st.success(f"✅ Reporte {pdf_label.get(rango_seleccionado, '')} generado exitosamente")
                else:
                    st.error(f"❌ Error del servidor: {response.status_code} - {response.text}")
        except Exception as e:
            st.error(f"❌ Error generando PDF: {str(e)}")

st.markdown("</div>", unsafe_allow_html=True)

# --- Nota de Advertencia ---
st.markdown("---")
st.warning("""
**⚠️ Nota importante:** 
La IA es una herramienta de soporte decisional. 
La validación clínica final y la responsabilidad del diagnóstico recaen exclusivamente en el profesional de salud.
""")