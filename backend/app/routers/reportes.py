from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from typing import List, Dict, Any
from fpdf import FPDF
import io
import httpx
from app.config import settings

from app.database import get_db
from app.dependencies import GerenteDep, AuditorDep, CurrentUser
from app.models.triaje import Triaje
from app.models.paciente import Paciente
from app.models.sintoma_triaje import SintomaTriaje
from sqlalchemy import and_, extract

router = APIRouter(prefix="/api/v1/reportes", tags=["Reportes"])

async def notificar_reporte_generado(tipo_reporte: str, params: Dict[str, Any] = None):
    """Notifica a n8n que se generó un reporte para enviar email"""
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            payload = {
                "origen": "fastapi",
                "tipo_reporte": tipo_reporte,
                "timestamp": datetime.now().isoformat(),
                "params": params or {}
            }
            
            # URL del webhook de n8n (ajustar según tu deploy)
            webhook_url = "https://n8n-production-d937.up.railway.app/webhook/generar-reporte"
            
            response = await client.post(webhook_url, json=payload)
            response.raise_for_status()
            
            # Log de notificación exitosa (opcional)
            print(f"✅ Notificación enviada a n8n: {tipo_reporte}")
            
    except httpx.HTTPStatusError as e:
        print(f"⚠️ Error HTTP notificando a n8n: {e}")
    except httpx.TimeoutException:
        print(f"⚠️ Timeout notificando a n8n")
    except Exception as e:
        print(f"⚠️ Error notificando a n8n: {e}")
    # No lanzar excepción para no bloquear la generación del reporte

class PDFReport(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'Sistema de Triaje Clinico - Reporte Operativo', 0, 1, 'C')
        self.set_font('Arial', '', 8)
        self.cell(0, 5, 'Hospital Clinico - Unidad de Emergencia', 0, 1, 'C')
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Pagina {self.page_no()} | Generado automaticamente', 0, 0, 'C')

@router.get("/shift-pdf")
async def generate_shift_report(
    rango: str = Query("hoy", description="Rango: hoy, mes, total"),
    db: AsyncSession = Depends(get_db)
):
    """Genera reporte PDF del turno/periodo seleccionado"""
    hoy = datetime.now().date()
    
    # Determinar rango de fechas
    if rango == "hoy":
        fecha_inicio = datetime.combine(hoy, datetime.min.time())
        fecha_fin = datetime.combine(hoy, datetime.max.time())
        titulo_rango = hoy.strftime("%d/%m/%Y")
    elif rango == "mes":
        fecha_inicio = datetime.combine(hoy.replace(day=1), datetime.min.time())
        fecha_fin = datetime.combine(hoy, datetime.max.time())
        titulo_rango = f"{hoy.strftime('%B %Y')}"
    else:  # total
        fecha_inicio = datetime(2000, 1, 1)
        fecha_fin = datetime.combine(hoy, datetime.max.time())
        titulo_rango = "Historico Total"
    
    # Obtener datos del período
    result = await db.execute(
        select(Triaje, Paciente)
        .join(Paciente, Triaje.paciente_id == Paciente.id)
        .where(
            and_(
                Triaje.created_at >= fecha_inicio,
                Triaje.created_at <= fecha_fin
            )
        )
        .order_by(Triaje.created_at)
    )
    rows = result.all()
    
    # Calcular estadísticas
    total_triajes = len(rows)
    confirmados_ia = sum(1 for t, p in rows if t.nivel_urgencia_asignado_ia == t.nivel_urgencia_final)
    discrepancias = total_triajes - confirmados_ia
    tasa_confirmacion = round((confirmados_ia / total_triajes * 100), 1) if total_triajes > 0 else 0
    
    # Conteo por nivel de urgencia
    conteo_urgencia = {}
    for triaje, paciente in rows:
        nivel = triaje.nivel_urgencia_final or 'SIN_CLASIFICAR'
        conteo_urgencia[nivel] = conteo_urgencia.get(nivel, 0) + 1
    
    # Crear PDF
    pdf = PDFReport()
    pdf.add_page()
    
    # Titulo
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(0, 10, 'Reporte de Turno - Sistema de Triaje', 0, 1, 'C')
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 8, f'Periodo: {titulo_rango}', 0, 1, 'C')
    pdf.ln(5)
    
    # Seccion de Resumen
    pdf.set_font('Arial', 'B', 11)
    pdf.set_fill_color(230, 230, 230)
    pdf.cell(0, 8, 'RESUMEN ESTADISTICO', 1, 1, 'L', True)
    pdf.ln(2)
    
    pdf.set_font('Arial', '', 10)
    pdf.cell(80, 7, f'Total de Triajes: {total_triajes}', 0, 0)
    pdf.cell(80, 7, f'Confirmados IA: {confirmados_ia} ({tasa_confirmacion}%)', 0, 1)
    pdf.cell(80, 7, f'Discrepancias IA/Enfermera: {discrepancias}', 0, 0)
    pdf.cell(80, 7, f'Generado: {datetime.now().strftime("%d/%m/%Y %H:%M")}', 0, 1)
    pdf.ln(5)
    
    # Distribucion por nivel de urgencia
    if conteo_urgencia:
        pdf.set_font('Arial', 'B', 10)
        pdf.cell(0, 7, 'Distribucion por Nivel de Urgencia:', 0, 1)
        pdf.set_font('Arial', '', 9)
        niveles_orden = ['RED', 'ORANGE', 'YELLOW', 'GREEN', 'BLUE']
        etiquetas = {
            'RED': 'Critico (RED)',
            'ORANGE': 'Urgente (ORANGE)',
            'YELLOW': 'Poco Urgente (YELLOW)',
            'GREEN': 'No Urgente (GREEN)',
            'BLUE': 'Administrativo (BLUE)'
        }
        pdf.ln(3)
        for nivel in niveles_orden:
            if nivel in conteo_urgencia:
                etiqueta = etiquetas.get(nivel, nivel)
                pdf.cell(80, 6, f'- {etiqueta}: {conteo_urgencia[nivel]} pacientes', 0, 1)
        pdf.ln(5)
    
    # Tabla de detalle
    if rows:
        pdf.set_font('Arial', 'B', 11)
        pdf.set_fill_color(200, 200, 200)
        pdf.cell(0, 8, 'DETALLE DE TRIAJES', 1, 1, 'L', True)
        pdf.ln(2)
        
        # Encabezados de tabla
        pdf.set_font('Arial', 'B', 8)
        pdf.set_fill_color(240, 240, 240)
        pdf.cell(25, 8, 'Hora', 1, 0, 'C', True)
        pdf.cell(45, 8, 'Paciente', 1, 0, 'C', True)
        pdf.cell(45, 8, 'Motivo', 1, 0, 'C', True)
        pdf.cell(20, 8, 'IA Sug.', 1, 0, 'C', True)
        pdf.cell(20, 8, 'Nivel Final', 1, 0, 'C', True)
        pdf.cell(20, 8, 'Tiempo', 1, 0, 'C', True)
        pdf.cell(20, 8, 'Estado', 1, 1, 'C', True)
        
        # Datos
        pdf.set_font('Arial', '', 7)
        for triaje, paciente in rows:
            # Hora
            pdf.cell(25, 6, triaje.created_at.strftime("%d/%m %H:%M"), 1, 0, 'C')
            # Paciente
            nombre = f"{paciente.nombres} {paciente.apellidos}"[:22]
            pdf.cell(45, 6, nombre, 1, 0, 'L')
            # Motivo
            motivo = (triaje.motivo_consulta or '-')[:25]
            pdf.cell(45, 6, motivo, 1, 0, 'L')
            # IA Sugerido
            nivel_ia = triaje.nivel_urgencia_asignado_ia or '-'
            pdf.cell(20, 6, nivel_ia, 1, 0, 'C')
            # Nivel Final
            nivel_final = triaje.nivel_urgencia_final or '-'
            pdf.cell(20, 6, nivel_final, 1, 0, 'C')
            # Tiempo (convertir segundos a minutos)
            tiempo_min = round(triaje.tiempo_atencion_segundos / 60, 1) if triaje.tiempo_atencion_segundos else '-'
            pdf.cell(20, 6, str(tiempo_min), 1, 0, 'C')
            # Estado
            estado = triaje.estado_logistico or 'N/A'
            pdf.cell(20, 6, estado[:10], 1, 1, 'C')
    else:
        pdf.set_font('Arial', 'I', 10)
        pdf.cell(0, 10, 'No hay triajes registrados en este periodo.', 0, 1, 'C')
    
    # Pie de pagina con info adicional
    pdf.ln(10)
    pdf.set_font('Arial', 'I', 8)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 5, 'Reporte generado por: Sistema', 0, 1, 'L')
    pdf.cell(0, 5, 'Sistema de Triaje Clinico Asistido por IA - Hospital Clinico', 0, 1, 'L')
    
    # Exportar
    output = io.BytesIO()
    pdf.output(output)
    output.seek(0)
    
    filename = f"reporte_turno_{rango}_{hoy.strftime('%Y%m%d')}.pdf"
    
    # Notificar a n8n para enviar email
    await notificar_reporte_generado("shift-pdf", {"rango": rango, "filename": filename})
    
    return StreamingResponse(
        output,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )

@router.get("/monthly-pdf")
async def generate_monthly_report_pdf(
    mes: int = Query(..., description="Mes (1-12)", ge=1, le=12),
    anio: int = Query(..., description="Año (YYYY)", ge=2020, le=2030),
    db: AsyncSession = Depends(get_db),
    current_user: GerenteDep = None
):
    """
    Genera reporte PDF mensual completo con:
    - Resumen ejecutivo
    - Distribución por nivel de urgencia
    - Tabla de discrepancias IA vs Humano
    - Tiempos promedio
    """
    # Calcular rango de fechas
    fecha_inicio = datetime(anio, mes, 1)
    if mes == 12:
        fecha_fin = datetime(anio + 1, 1, 1) - timedelta(seconds=1)
    else:
        fecha_fin = datetime(anio, mes + 1, 1) - timedelta(seconds=1)
    
    nombre_mes = fecha_inicio.strftime("%B %Y").upper()
    
    # --- KPIs ---
    result = await db.execute(
        select(func.count()).select_from(Triaje)
        .where(
            and_(
                Triaje.created_at >= fecha_inicio,
                Triaje.created_at <= fecha_fin,
                Triaje.activo == True
            )
        )
    )
    total_casos = result.scalar() or 0
    
    # Concordancia IA
    result = await db.execute(
        select(func.count()).select_from(Triaje)
        .where(
            and_(
                Triaje.created_at >= fecha_inicio,
                Triaje.created_at <= fecha_fin,
                Triaje.nivel_urgencia_asignado_ia == Triaje.nivel_urgencia_final
            )
        )
    )
    coincidencias = result.scalar() or 0
    discrepancias = total_casos - coincidencias
    tasa_concordancia = round((coincidencias / total_casos * 100), 1) if total_casos > 0 else 0
    
    # Tiempo promedio
    result = await db.execute(
        select(func.avg(Triaje.tiempo_atencion_segundos))
        .where(
            and_(
                Triaje.created_at >= fecha_inicio,
                Triaje.created_at <= fecha_fin,
                Triaje.tiempo_atencion_segundos != None
            )
        )
    )
    tiempo_seg = result.scalar() or 0
    tiempo_promedio = round(tiempo_seg / 60, 1) if tiempo_seg else 0
    
    # Críticos (RED)
    result = await db.execute(
        select(func.count()).select_from(Triaje)
        .where(
            and_(
                Triaje.created_at >= fecha_inicio,
                Triaje.created_at <= fecha_fin,
                Triaje.nivel_urgencia_final == "RED"
            )
        )
    )
    criticos = result.scalar() or 0
    
    # --- Distribución por nivel ---
    niveles = ["RED", "ORANGE", "YELLOW", "GREEN", "BLUE"]
    distribucion = {}
    for nivel in niveles:
        result = await db.execute(
            select(func.count()).select_from(Triaje)
            .where(
                and_(
                    Triaje.created_at >= fecha_inicio,
                    Triaje.created_at <= fecha_fin,
                    Triaje.nivel_urgencia_final == nivel
                )
            )
        )
        distribucion[nivel] = result.scalar() or 0
    
    # --- Discrepancias detalladas ---
    result = await db.execute(
        select(Triaje, Paciente)
        .join(Paciente, Triaje.paciente_id == Paciente.id)
        .where(
            and_(
                Triaje.created_at >= fecha_inicio,
                Triaje.created_at <= fecha_fin,
                Triaje.nivel_urgencia_asignado_ia != Triaje.nivel_urgencia_final
            )
        )
        .order_by(Triaje.created_at.desc())
    )
    discrepancias_rows = result.all()
    
    # Crear PDF
    pdf = PDFReport()
    pdf.add_page()
    pdf.alias_nb_pages()
    
    # Título
    pdf.set_font('Arial', 'B', 18)
    pdf.cell(0, 10, 'SISTEMA DE TRIAJE CLÍNICO', 0, 1, 'C')
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(0, 8, 'REPORTE MENSUAL', 0, 1, 'C')
    pdf.set_font('Arial', '', 12)
    pdf.cell(0, 6, f'Período: {nombre_mes}', 0, 1, 'C')
    pdf.ln(10)
    
    # === RESUMEN EJECUTIVO ===
    pdf.set_font('Arial', 'B', 12)
    pdf.set_fill_color(230, 230, 230)
    pdf.cell(0, 8, 'RESUMEN EJECUTIVO', 1, 1, 'L', True)
    pdf.ln(2)
    
    pdf.set_font('Arial', '', 10)
    resumen_texto = (
        f"Durante {nombre_mes}, se registraron {total_casos} triajes. La tasa de concurrencia "
        f"entre IA y enfermería fue del {tasa_concordancia}%, con {discrepancias} casos de discrepancia. "
        f"El tiempo promedio de atención fue {tiempo_promedio} minutos. "
        f"Se atendieron {criticos} pacientes críticos (nivel RED)."
    )
    pdf.multi_cell(0, 6, resumen_texto)
    pdf.ln(5)
    
    # === KPIs EN TABLA ===
    pdf.set_font('Arial', 'B', 11)
    pdf.cell(0, 7, 'INDICADORES CLAVE', 0, 1)
    pdf.ln(2)
    
    # Tabla de KPIs
    pdf.set_font('Arial', 'B', 9)
    pdf.set_fill_color(240, 240, 240)
    pdf.cell(50, 7, 'Indicador', 1, 0, 'C', True)
    pdf.cell(40, 7, 'Valor', 1, 0, 'C', True)
    pdf.cell(60, 7, 'Benchmark', 1, 1, 'C', True)
    
    pdf.set_font('Arial', '', 9)
    kpis = [
        ("Total de Triajes", str(total_casos), "-"),
        ("Tasa Concordancia IA", f"{tasa_concordancia}%", "> 85%"),
        ("Tiempo Promedio", f"{tiempo_promedio} min", "< 15 min"),
        ("Pacientes Críticos", str(criticos), "Prioridad máxima"),
        ("Discrepancias", str(discrepancias), "Revisar casos"),
    ]
    
    for indicador, valor, benchmark in kpis:
        pdf.cell(50, 7, indicador, 1, 0, 'L')
        pdf.cell(40, 7, valor, 1, 0, 'C')
        pdf.cell(60, 7, benchmark, 1, 1, 'C')
    pdf.ln(5)
    
    # === DISTRIBUCIÓN POR NIVEL ===
    pdf.set_font('Arial', 'B', 11)
    pdf.cell(0, 7, 'DISTRIBUCIÓN POR NIVEL DE URGENCIA', 0, 1)
    pdf.ln(2)
    
    pdf.set_font('Arial', 'B', 9)
    pdf.set_fill_color(240, 240, 240)
    pdf.cell(40, 7, 'Nivel', 1, 0, 'C', True)
    pdf.cell(40, 7, 'Cantidad', 1, 0, 'C', True)
    pdf.cell(40, 7, 'Porcentaje', 1, 0, 'C', True)
    pdf.cell(50, 7, 'Barra', 1, 1, 'C', True)
    
    pdf.set_font('Arial', '', 9)
    colores_nivel = {
        'RED': (255, 200, 200),
        'ORANGE': (255, 220, 180),
        'YELLOW': (255, 255, 200),
        'GREEN': (200, 255, 200),
        'BLUE': (200, 220, 255),
    }
    
    for nivel in niveles:
        cantidad = distribucion[nivel]
        porcentaje = round((cantidad / total_casos * 100), 1) if total_casos > 0 else 0
        # Calcular ancho de barra (máximo 50mm, 0 si porcentaje es 0)
        barra_width = min(50, max(0, porcentaje / 2)) if porcentaje > 0 else 0
        
        # Color de fondo para la fila
        if nivel in colores_nivel:
            pdf.set_fill_color(*colores_nivel[nivel])
        else:
            pdf.set_fill_color(255, 255, 255)
        
        pdf.cell(40, 7, nivel, 1, 0, 'C', True)
        pdf.cell(40, 7, str(cantidad), 1, 0, 'C', True)
        pdf.cell(40, 7, f"{porcentaje}%", 1, 0, 'C', True)
        
        # Barra visual (celda fija de 50mm total)
        # Si hay barra, dibujar barra + espacio restante
        # Si no hay barra, dibujar celda vacía de 50mm completa
        pdf.set_fill_color(100, 100, 100)
        if barra_width > 0:
            pdf.cell(barra_width, 7, '', 0, 0, 'C', True)
            if 50 - barra_width > 0:
                pdf.cell(50 - barra_width, 7, '', 0, 0, 'C', False)
            else:
                pdf.cell(0.1, 7, '', 0, 0, 'C', False)  # Mínimo para evitar overflow
        else:
            # Sin barra - celda vacía de ancho fijo
            pdf.cell(50, 7, '', 0, 0, 'C', False)
        pdf.ln(7)
    pdf.ln(3)
    
    # === TABLA DE DISCREPANCIAS ===
    if discrepancias_rows:
        pdf.add_page()
        pdf.set_font('Arial', 'B', 12)
        pdf.set_fill_color(230, 230, 230)
        pdf.cell(0, 8, 'TABLA DE DISCREPANCIAS IA vs HUMANO', 1, 1, 'L', True)
        pdf.ln(2)
        
        # Encabezados
        pdf.set_font('Arial', 'B', 8)
        pdf.set_fill_color(240, 240, 240)
        pdf.cell(25, 8, 'Fecha', 1, 0, 'C', True)
        pdf.cell(45, 8, 'Paciente', 1, 0, 'C', True)
        pdf.cell(25, 8, 'Nivel IA', 1, 0, 'C', True)
        pdf.cell(30, 8, 'Nivel Humano', 1, 0, 'C', True)
        pdf.cell(50, 8, 'Discrepancia', 1, 1, 'C', True)
        
        # Datos (máximo 50 filas por página)
        pdf.set_font('Arial', '', 8)
        for i, (triaje, paciente) in enumerate(discrepancias_rows[:50]):
            if pdf.get_y() > 250:  # Si queda poco espacio
                pdf.add_page()
                pdf.set_font('Arial', 'B', 8)
                pdf.cell(25, 8, 'Fecha', 1, 0, 'C', True)
                pdf.cell(45, 8, 'Paciente', 1, 0, 'C', True)
                pdf.cell(25, 8, 'Nivel IA', 1, 0, 'C', True)
                pdf.cell(30, 8, 'Nivel Humano', 1, 0, 'C', True)
                pdf.cell(50, 8, 'Discrepancia', 1, 1, 'C', True)
                pdf.set_font('Arial', '', 8)
            
            fecha = triaje.created_at.strftime("%d/%m/%Y") if triaje.created_at else '-'
            nombre = f"{paciente.nombres} {paciente.apellidos}"[:20]
            nivel_ia = triaje.nivel_urgencia_asignado_ia or '-'
            nivel_humano = triaje.nivel_urgencia_final or '-'
            
            # Determinar tipo de discrepancia
            niveles_orden = {'RED': 5, 'ORANGE': 4, 'YELLOW': 3, 'GREEN': 2, 'BLUE': 1}
            val_ia = niveles_orden.get(nivel_ia, 0)
            val_hum = niveles_orden.get(nivel_humano, 0)
            if val_hum > val_ia:
                tipo_disc = "Sobre-clasificación"
            elif val_hum < val_ia:
                tipo_disc = "Sub-clasificación"
            else:
                tipo_disc = "Diferente nivel"
            
            pdf.cell(25, 6, fecha, 1, 0, 'C')
            pdf.cell(45, 6, nombre, 1, 0, 'L')
            pdf.cell(25, 6, nivel_ia, 1, 0, 'C')
            pdf.cell(30, 6, nivel_humano, 1, 0, 'C')
            pdf.cell(50, 6, tipo_disc, 1, 1, 'C')
        
        if len(discrepancias_rows) > 50:
            pdf.ln(5)
            pdf.set_font('Arial', 'I', 9)
            pdf.cell(0, 6, f'... y {len(discrepancias_rows) - 50} discrepancias más', 0, 1, 'C')
    
    # Pie de página con info
    pdf.ln(10)
    pdf.set_font('Arial', 'I', 8)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 5, f'Reporte generado automáticamente el {datetime.now().strftime("%d/%m/%Y %H:%M")}', 0, 1, 'C')
    pdf.cell(0, 5, 'Sistema de Triaje Clínico Asistido por IA - Hospital Clínico', 0, 1, 'C')
    
    # Exportar
    output = io.BytesIO()
    pdf.output(output)
    output.seek(0)
    
    filename = f"reporte_mensual_{mes:02d}_{anio}.pdf"
    
    # Notificar a n8n para enviar email
    await notificar_reporte_generado("monthly-pdf", {"mes": mes, "anio": anio, "filename": filename})
    
    return StreamingResponse(
        output,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )


@router.get("/shift-pdf-gerente")
async def generate_shift_report_gerente(
    start_date: str = Query(..., description="YYYY-MM-DD"),
    end_date: str = Query(..., description="YYYY-MM-DD"),
    db: AsyncSession = Depends(get_db),
    current_user: GerenteDep = None
):
    """Genera reporte PDF avanzado para gerencia con rango de fechas personalizado"""
    # (Misma implementacion mejorada pero con fechas personalizadas)
    fecha_inicio = datetime.strptime(start_date, "%Y-%m-%d")
    fecha_fin = datetime.strptime(end_date, "%Y-%m-%d").replace(hour=23, minute=59, second=59)
    
    # Obtener datos del periodo
    result = await db.execute(
        select(Triaje, Paciente)
        .join(Paciente, Triaje.paciente_id == Paciente.id)
        .where(
            and_(
                Triaje.created_at >= fecha_inicio,
                Triaje.created_at <= fecha_fin
            )
        )
        .order_by(Triaje.created_at)
    )
    rows = result.all()
    
    # Calcular estadísticas
    total_triajes = len(rows)
    confirmados_ia = sum(1 for t, p in rows if t.nivel_urgencia_asignado_ia == t.nivel_urgencia_final)
    tasa_confirmacion = round((confirmados_ia / total_triajes * 100), 1) if total_triajes > 0 else 0
    
    # Crear PDF con encabezado gerencial
    pdf = PDFReport()
    pdf.add_page()
    
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(0, 10, 'Reporte Gerencial - Sistema de Triaje', 0, 1, 'C')
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 8, f'Periodo: {fecha_inicio.strftime("%d/%m/%Y")} al {fecha_fin.strftime("%d/%m/%Y")}', 0, 1, 'C')
    pdf.ln(5)
    
    # Resumen estadistico
    pdf.set_font('Arial', 'B', 11)
    pdf.cell(0, 8, 'RESUMEN EJECUTIVO', 1, 1, 'L', True)
    pdf.ln(2)
    
    pdf.set_font('Arial', '', 10)
    pdf.cell(0, 7, f'Total de Triajes: {total_triajes}', 0, 1)
    pdf.cell(0, 7, f'Precision IA: {tasa_confirmacion}% ({confirmados_ia}/{total_triajes})', 0, 1)
    pdf.ln(5)
    
    # Tabla detallada
    if rows:
        pdf.set_font('Arial', 'B', 8)
        pdf.cell(30, 8, 'Fecha/Hora', 1, 0, 'C', True)
        pdf.cell(50, 8, 'Paciente', 1, 0, 'C', True)
        pdf.cell(50, 8, 'Motivo', 1, 0, 'C', True)
        pdf.cell(20, 8, 'IA', 1, 0, 'C', True)
        pdf.cell(20, 8, 'Final', 1, 0, 'C', True)
        pdf.cell(25, 8, 'Estado', 1, 1, 'C', True)
        
        pdf.set_font('Arial', '', 7)
        for triaje, paciente in rows:
            pdf.cell(30, 6, triaje.created_at.strftime("%d/%m %H:%M"), 1, 0, 'C')
            pdf.cell(50, 6, f"{paciente.nombres} {paciente.apellidos}"[:25], 1, 0, 'L')
            pdf.cell(50, 6, (triaje.motivo_consulta or '-')[:28], 1, 0, 'L')
            pdf.cell(20, 6, triaje.nivel_urgencia_asignado_ia or '-', 1, 0, 'C')
            pdf.cell(20, 6, triaje.nivel_urgencia_final or '-', 1, 0, 'C')
            pdf.cell(25, 6, triaje.estado_logistico or 'N/A', 1, 1, 'C')
    else:
        pdf.cell(0, 10, 'No hay datos en el periodo seleccionado.', 0, 1, 'C')
    
    output = io.BytesIO()
    pdf.output(output)
    output.seek(0)
    
    filename = f"reporte_gerencial_{fecha_inicio.strftime('%Y%m%d')}_{fecha_fin.strftime('%Y%m%d')}.pdf"
    
    return StreamingResponse(
        output,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )


@router.get("/dashboard")
async def get_dashboard_data(
    start_date: str = Query(..., description="YYYY-MM-DD"),
    end_date: str = Query(..., description="YYYY-MM-DD"),
    db: AsyncSession = Depends(get_db),
    current_user: GerenteDep = None
):
    """Datos para dashboard de gestion"""
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")
    
    # Volumen mensual por nivel de urgencia
    result_volumen = await db.execute(
        select(
            func.date_trunc('month', Triaje.created_at).label('mes'),
            Triaje.nivel_urgencia_final,
            func.count().label('total')
        )
        .where(Triaje.created_at.between(start, end))
        .group_by('mes', Triaje.nivel_urgencia_final)
        .order_by('mes')
    )
    
    # Transformar a formato pivotado para el frontend (mes -> RED, ORANGE, YELLOW, GREEN, BLUE)
    from collections import defaultdict
    volumen_pivot = defaultdict(lambda: {"RED": 0, "ORANGE": 0, "YELLOW": 0, "GREEN": 0, "BLUE": 0})
    
    for row in result_volumen.all():
        mes_key = row.mes.strftime("%Y-%m") if hasattr(row.mes, 'strftime') else str(row.mes)[:7]
        nivel = row.nivel_urgencia_final or "BLUE"  # Default para no asignados
        if nivel in volumen_pivot[mes_key]:
            volumen_pivot[mes_key][nivel] = row.total
    
    volumen_mensual = [
        {"mes": mes, **counts}
        for mes, counts in sorted(volumen_pivot.items())
    ]
    
    # Comparativa IA vs Enfermería por nivel de urgencia
    # Contar sugerencias de IA por nivel
    result_ia = await db.execute(
        select(
            Triaje.nivel_urgencia_asignado_ia.label('nivel'),
            func.count().label('total')
        )
        .where(
            Triaje.created_at.between(start, end),
            Triaje.nivel_urgencia_asignado_ia.isnot(None)
        )
        .group_by(Triaje.nivel_urgencia_asignado_ia)
    )
    
    # Contar confirmaciones de enfermera por nivel
    result_humano = await db.execute(
        select(
            Triaje.nivel_urgencia_final.label('nivel'),
            func.count().label('total')
        )
        .where(
            Triaje.created_at.between(start, end),
            Triaje.nivel_urgencia_final.isnot(None)
        )
        .group_by(Triaje.nivel_urgencia_final)
    )
    
    # Crear diccionarios para lookup
    ia_counts = {row.nivel: row.total for row in result_ia.all()}
    humano_counts = {row.nivel: row.total for row in result_humano.all()}
    
    # Construir array en formato que espera el frontend
    all_niveles = set(ia_counts.keys()) | set(humano_counts.keys())
    comparativa_confianza = [
        {
            "nivel": nivel,
            "ia": ia_counts.get(nivel, 0),
            "humano": humano_counts.get(nivel, 0)
        }
        for nivel in sorted(all_niveles)
    ]
    
    # Calcular coincidencias y discrepancias IA vs Humano
    coincidencias = sum(ia_counts.get(nivel, 0) for nivel in all_niveles if ia_counts.get(nivel, 0) == humano_counts.get(nivel, 0))
    discrepancias = sum(ia_counts.get(nivel, 0) for nivel in all_niveles if ia_counts.get(nivel, 0) != humano_counts.get(nivel, 0))
    
    # Tiempo promedio semanal
    result_tiempo = await db.execute(
        select(
            func.date_trunc('week', Triaje.created_at).label('semana'),
            func.avg(Triaje.tiempo_atencion_segundos).label('promedio')
        )
        .where(
            Triaje.created_at.between(start, end),
            Triaje.tiempo_atencion_segundos.isnot(None)
        )
        .group_by('semana')
        .order_by('semana')
    )
    
    tiempo_promedio_semanal = [
        {
            "semana": row.semana.strftime("%Y-W%U") if hasattr(row.semana, 'strftime') else str(row.semana)[:10],
            "promedio": round((row.promedio or 0) / 60, 1),
            "meta": 5  # Meta de 5 minutos
        }
        for row in result_tiempo.all()
    ]
    
    # KPIs
    total = await db.scalar(select(func.count()).select_from(Triaje).where(Triaje.created_at.between(start, end)))
    tiempo_promedio = await db.scalar(
        select(func.avg(Triaje.tiempo_atencion_segundos)).where(Triaje.created_at.between(start, end))
    )
    
    # Calcular tasa de concordancia IA
    total_con_ia = coincidencias + discrepancias
    tasa_concordancia = round((coincidencias / total_con_ia) * 100, 1) if total_con_ia > 0 else 0
    
    # Contar críticos atendidos (RED)
    criticos = await db.scalar(
        select(func.count())
        .select_from(Triaje)
        .where(
            Triaje.created_at.between(start, end),
            Triaje.nivel_urgencia_final == "RED"
        )
    )
    
    return {
        "kpis": {
            "total_triajes": total or 0,
            "promedio_tiempo": round((tiempo_promedio or 0) / 60, 1),
            "tasa_concurrencia_ia": tasa_concordancia,
            "criticos_atendidos": criticos or 0
        },
        "volumen_mensual": volumen_mensual,
        "comparativa_confianza": comparativa_confianza,
        "tiempo_promedio_semanal": tiempo_promedio_semanal
    }


@router.get("/dashboard-operativo", response_model=Dict[str, Any])
async def get_dashboard_operativo(
    rango: str = Query("hoy", description="Rango de fechas: hoy, mes, total"),
    db: AsyncSession = Depends(get_db),
    current_user: CurrentUser = None
):
    """
    Datos en tiempo real para el dashboard operativo de enfermeria.
    Metricas del dia actual, mes actual o historico total.
    
    Parametros:
    - rango: "hoy" (dia actual), "mes" (mes actual), "total" (historico completo)
    """
    hoy = datetime.now().date()
    
    if rango == "hoy":
        fecha_inicio = datetime.combine(hoy, datetime.min.time())
        fecha_fin = datetime.combine(hoy, datetime.max.time())
        titulo_rango = "Hoy"
    elif rango == "mes":
        # Primer dia del mes actual
        fecha_inicio = datetime.combine(hoy.replace(day=1), datetime.min.time())
        fecha_fin = datetime.combine(hoy, datetime.max.time())
        titulo_rango = "Este Mes"
    elif rango == "total":
        # Todo el historico
        fecha_inicio = datetime(2000, 1, 1)
        fecha_fin = datetime.combine(hoy, datetime.max.time())
        titulo_rango = "Historico Total"
    else:
        # Default: hoy
        fecha_inicio = datetime.combine(hoy, datetime.min.time())
        fecha_fin = datetime.combine(hoy, datetime.max.time())
        titulo_rango = "Hoy"
    
    # --- KPI 1: Triajes en espera (estado_logistico = 'En Espera') - SIEMPRE ACTUAL ---
    result = await db.execute(
        select(func.count()).select_from(Triaje)
        .where(
            and_(
                Triaje.estado_logistico == "En Espera",
                Triaje.activo == True
            )
        )
    )
    en_espera = result.scalar() or 0
    
    # --- KPI 2: Tiempo promedio de triaje en el rango ---
    result = await db.execute(
        select(func.avg(Triaje.tiempo_atencion_segundos))
        .where(
            and_(
                Triaje.created_at.between(fecha_inicio, fecha_fin),
                Triaje.tiempo_atencion_segundos != None
            )
        )
    )
    tiempo_promedio_seg = result.scalar() or 0
    tiempo_promedio_min = round(tiempo_promedio_seg / 60, 1)
    
    # --- KPI 3: Pacientes criticos (RED/ORANGE) en espera - SIEMPRE ACTUAL ---
    result = await db.execute(
        select(func.count()).select_from(Triaje)
        .where(
            and_(
                Triaje.estado_logistico == "En Espera",
                Triaje.nivel_urgencia_final.in_(["RED", "ORANGE"]),
                Triaje.activo == True
            )
        )
    )
    criticos = result.scalar() or 0
    
    # --- Top Sintomas del rango ---
    result = await db.execute(
        select(
            SintomaTriaje.sintoma,
            func.count().label("frecuencia")
        )
        .join(Triaje, SintomaTriaje.triaje_id == Triaje.id)
        .where(Triaje.created_at.between(fecha_inicio, fecha_fin))
        .group_by(SintomaTriaje.sintoma)
        .order_by(func.count().desc())
        .limit(10)
    )
    sintomas_rows = result.all()
    top_sintomas = [
        {"sintoma": row.sintoma, "frecuencia": row.frecuencia}
        for row in sintomas_rows
    ]
    
    # --- Flujo por periodo ---
    flujo_por_hora = []
    if rango == "hoy":
        # Por horas para el dia actual
        for hora in range(24):
            hora_inicio = fecha_inicio + timedelta(hours=hora)
            hora_fin = fecha_inicio + timedelta(hours=hora+1)
            result = await db.execute(
                select(func.count()).select_from(Triaje)
                .where(
                    and_(
                        Triaje.created_at >= hora_inicio,
                        Triaje.created_at < hora_fin
                    )
                )
            )
            count = result.scalar() or 0
            flujo_por_hora.append({"hora": hora, "llegadas": count})
    elif rango == "mes":
        # Por dias para el mes actual
        dias_mes = hoy.day
        for dia in range(1, dias_mes + 1):
            dia_fecha = hoy.replace(day=dia)
            dia_inicio = datetime.combine(dia_fecha, datetime.min.time())
            dia_fin = datetime.combine(dia_fecha, datetime.max.time())
            result = await db.execute(
                select(func.count()).select_from(Triaje)
                .where(
                    and_(
                        Triaje.created_at >= dia_inicio,
                        Triaje.created_at <= dia_fin
                    )
                )
            )
            count = result.scalar() or 0
            flujo_por_hora.append({"hora": dia, "llegadas": count})  # 'hora' se usa como dia
    else:  # total - por meses
        # Agrupar por meses (últimos 12 meses)
        for mes_offset in range(11, -1, -1):
            mes_fecha = hoy.replace(day=1) - relativedelta(months=mes_offset)
            mes_fin = (mes_fecha + relativedelta(months=1) - timedelta(days=1))
            result = await db.execute(
                select(func.count()).select_from(Triaje)
                .where(
                    and_(
                        Triaje.created_at >= datetime.combine(mes_fecha, datetime.min.time()),
                        Triaje.created_at <= datetime.combine(mes_fin, datetime.max.time())
                    )
                )
            )
            count = result.scalar() or 0
            flujo_por_hora.append({"hora": mes_fecha.strftime("%b"), "llegadas": count})
    
    # --- Distribucion por nivel de urgencia (en espera actualmente) ---
    niveles = ["RED", "ORANGE", "YELLOW", "GREEN", "BLUE"]
    distribucion = []
    for nivel in niveles:
        result = await db.execute(
            select(func.count()).select_from(Triaje)
            .where(
                and_(
                    Triaje.estado_logistico == "En Espera",
                    Triaje.nivel_urgencia_final == nivel,
                    Triaje.activo == True
                )
            )
        )
        count = result.scalar() or 0
        distribucion.append({"nivel": nivel, "cantidad": count})
    
    # --- Resumen del periodo ---
    result = await db.execute(
        select(func.count()).select_from(Triaje)
        .where(Triaje.created_at.between(fecha_inicio, fecha_fin))
    )
    total_periodo = result.scalar() or 0
    
    result = await db.execute(
        select(func.count()).select_from(Triaje)
        .where(
            and_(
                Triaje.created_at.between(fecha_inicio, fecha_fin),
                Triaje.nivel_urgencia_asignado_ia == Triaje.nivel_urgencia_final
            )
        )
    )
    confirmados_ia = result.scalar() or 0
    discrepancias = total_periodo - confirmados_ia if total_periodo > 0 else 0
    
    return {
        "rango": titulo_rango,
        "kpis": {
            "en_espera": en_espera,
            "tiempo_promedio_min": tiempo_promedio_min,
            "criticos": criticos,
            "total_periodo": total_periodo
        },
        "top_sintomas": top_sintomas,
        "flujo_por_hora": flujo_por_hora,
        "distribucion_urgencia": distribucion,
        "resumen_turno": {
            "total_atendidos": total_periodo,
            "confirmados_ia": confirmados_ia,
            "discrepancias": discrepancias,
            "tasa_confirmacion": round((confirmados_ia / total_periodo * 100), 1) if total_periodo > 0 else 0
        },
        "actualizado": datetime.now().isoformat()
    }


@router.get("/discrepancias")
async def get_discrepancias(
    start_date: str = Query(..., description="YYYY-MM-DD"),
    end_date: str = Query(..., description="YYYY-MM-DD"),
    db: AsyncSession = Depends(get_db),
    current_user: GerenteDep = None
):
    """
    Obtiene lista de discrepancias entre IA y enfermería.
    Muestra casos donde nivel_urgencia_asignado_ia != nivel_urgencia_final
    """
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")
    end = end.replace(hour=23, minute=59, second=59)
    
    result = await db.execute(
        select(Triaje, Paciente)
        .join(Paciente, Triaje.paciente_id == Paciente.id)
        .where(
            and_(
                Triaje.created_at >= start,
                Triaje.created_at <= end,
                Triaje.nivel_urgencia_asignado_ia != Triaje.nivel_urgencia_final,
                Triaje.activo == True
            )
        )
        .order_by(Triaje.created_at.desc())
    )
    rows = result.all()
    
    discrepancias = []
    for triaje, paciente in rows:
        # Calcular tipo de discrepancia
        niveles_orden = {'RED': 5, 'ORANGE': 4, 'YELLOW': 3, 'GREEN': 2, 'BLUE': 1}
        val_ia = niveles_orden.get(triaje.nivel_urgencia_asignado_ia, 0)
        val_hum = niveles_orden.get(triaje.nivel_urgencia_final, 0)
        
        if val_hum > val_ia:
            tipo = "Sobre-clasificacion"
        elif val_hum < val_ia:
            tipo = "Sub-clasificacion"
        else:
            tipo = "Diferente nivel"
        
        discrepancias.append({
            "id": triaje.id,
            "fecha": triaje.created_at.strftime("%Y-%m-%d"),
            "paciente": f"{paciente.nombres} {paciente.apellidos}",
            "nivel_ia": triaje.nivel_urgencia_asignado_ia,
            "nivel_humano": triaje.nivel_urgencia_final,
            "diferencia": abs(val_hum - val_ia),
            "tipo": tipo,
            "motivo_consulta": triaje.motivo_consulta
        })
    
    return discrepancias


@router.get("/discrepancias")
async def get_discrepancias(
    start_date: str = Query(..., description="YYYY-MM-DD"),
    end_date: str = Query(..., description="YYYY-MM-DD"),
    db: AsyncSession = Depends(get_db),
    current_user: GerenteDep = None
):
    """
    Obtiene lista de discrepancias entre IA y enfermeria.
    Muestra casos donde nivel_urgencia_asignado_ia != nivel_urgencia_final
    """
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")
    end = end.replace(hour=23, minute=59, second=59)
    
    result = await db.execute(
        select(Triaje, Paciente)
        .join(Paciente, Triaje.paciente_id == Paciente.id)
        .where(
            and_(
                Triaje.created_at >= start,
                Triaje.created_at <= end,
                Triaje.nivel_urgencia_asignado_ia != Triaje.nivel_urgencia_final,
                Triaje.activo == True
            )
        )
        .order_by(Triaje.created_at.desc())
    )
    rows = result.all()
    
    discrepancias = []
    for triaje, paciente in rows:
        # Calcular tipo de discrepancia
        niveles_orden = {'RED': 5, 'ORANGE': 4, 'YELLOW': 3, 'GREEN': 2, 'BLUE': 1}
        val_ia = niveles_orden.get(triaje.nivel_urgencia_asignado_ia, 0)
        val_hum = niveles_orden.get(triaje.nivel_urgencia_final, 0)
        
        if val_hum > val_ia:
            tipo = "Sobre-clasificacion"
        elif val_hum < val_ia:
            tipo = "Sub-clasificacion"
        else:
            tipo = "Diferente nivel"
        
        discrepancias.append({
            "id": triaje.id,
            "fecha": triaje.created_at.strftime("%Y-%m-%d"),
            "paciente": f"{paciente.nombres} {paciente.apellidos}",
            "nivel_ia": triaje.nivel_urgencia_asignado_ia,
            "nivel_humano": triaje.nivel_urgencia_final,
            "diferencia": abs(val_hum - val_ia),
            "tipo": tipo,
            "motivo_consulta": triaje.motivo_consulta
        })
    
    return discrepancias


@router.get("/analisis-auditoria")
async def get_analisis_auditoria(
    mes: int = Query(..., description="Mes (1-12)"),
    anio: int = Query(..., description="Año (YYYY)"),
    db: AsyncSession = Depends(get_db),
    current_user: AuditorDep = None
):
    """
    Datos anonimizados para análisis de auditoría.
    
    El auditor puede ver:
    - Estadísticas agregadas
    - Tendencias y patrones
    - Tasas de concordancia IA vs Humano
    - Tiempos de atención promedio
    
    NO incluye:
    - Nombres de pacientes
    - DNIs u otra información de identificación
    - Diagnósticos detallados
    - Notas médicas
    """
    # Calcular rango de fechas
    fecha_inicio = datetime(anio, mes, 1)
    if mes == 12:
        fecha_fin = datetime(anio + 1, 1, 1) - timedelta(seconds=1)
    else:
        fecha_fin = datetime(anio, mes + 1, 1) - timedelta(seconds=1)
    
    # --- KPIs Principales ---
    result = await db.execute(
        select(func.count()).select_from(Triaje)
        .where(
            and_(
                Triaje.created_at >= fecha_inicio,
                Triaje.created_at <= fecha_fin,
                Triaje.activo == True
            )
        )
    )
    total_casos = result.scalar() or 0
    
    # --- Concordancia IA vs Humano ---
    result = await db.execute(
        select(func.count()).select_from(Triaje)
        .where(
            and_(
                Triaje.created_at >= fecha_inicio,
                Triaje.created_at <= fecha_fin,
                Triaje.nivel_urgencia_asignado_ia == Triaje.nivel_urgencia_final
            )
        )
    )
    coincidencias = result.scalar() or 0
    
    discrepancias = total_casos - coincidencias
    tasa_concordancia = round((coincidencias / total_casos * 100), 1) if total_casos > 0 else 0
    
    # --- Distribución por nivel de urgencia (anonimizado) ---
    niveles = ["RED", "ORANGE", "YELLOW", "GREEN", "BLUE"]
    distribucion_urgencia = []
    for nivel in niveles:
        result = await db.execute(
            select(func.count()).select_from(Triaje)
            .where(
                and_(
                    Triaje.created_at >= fecha_inicio,
                    Triaje.created_at <= fecha_fin,
                    Triaje.nivel_urgencia_final == nivel
                )
            )
        )
        count = result.scalar() or 0
        porcentaje = round((count / total_casos * 100), 1) if total_casos > 0 else 0
        distribucion_urgencia.append({
            "nivel": nivel,
            "cantidad": count,
            "porcentaje": porcentaje
        })
    
    # --- Tiempos promedio por nivel de urgencia ---
    tiempos_por_nivel = []
    for nivel in niveles:
        result = await db.execute(
            select(func.avg(Triaje.tiempo_atencion_segundos))
            .where(
                and_(
                    Triaje.created_at >= fecha_inicio,
                    Triaje.created_at <= fecha_fin,
                    Triaje.nivel_urgencia_final == nivel,
                    Triaje.tiempo_atencion_segundos != None
                )
            )
        )
        tiempo_seg = result.scalar() or 0
        tiempo_min = round(tiempo_seg / 60, 1) if tiempo_seg else 0
        tiempos_por_nivel.append({
            "nivel": nivel,
            "tiempo_promedio_min": tiempo_min
        })
    
    # --- Tendencia diaria (solo conteos) ---
    tendencia_diaria = []
    for dia in range(1, 32):
        try:
            dia_fecha = datetime(anio, mes, dia)
            dia_inicio = dia_fecha.replace(hour=0, minute=0, second=0)
            dia_fin = dia_fecha.replace(hour=23, minute=59, second=59)
            
            result = await db.execute(
                select(func.count()).select_from(Triaje)
                .where(
                    and_(
                        Triaje.created_at >= dia_inicio,
                        Triaje.created_at <= dia_fin
                    )
                )
            )
            count = result.scalar() or 0
            
            result = await db.execute(
                select(func.count()).select_from(Triaje)
                .where(
                    and_(
                        Triaje.created_at >= dia_inicio,
                        Triaje.created_at <= dia_fin,
                        Triaje.nivel_urgencia_asignado_ia == Triaje.nivel_urgencia_final
                    )
                )
            )
            aciertos = result.scalar() or 0
            
            tendencia_diaria.append({
                "dia": dia,
                "total": count,
                "concordancias": aciertos,
                "discrepancias": count - aciertos
            })
        except ValueError:
            # Día no válido para ese mes
            break
    
    # --- Top síntomas (solo frecuencias, sin identificación) ---
    result = await db.execute(
        select(
            SintomaTriaje.sintoma,
            func.count().label("frecuencia")
        )
        .join(Triaje, SintomaTriaje.triaje_id == Triaje.id)
        .where(
            and_(
                Triaje.created_at >= fecha_inicio,
                Triaje.created_at <= fecha_fin
            )
        )
        .group_by(SintomaTriaje.sintoma)
        .order_by(func.count().desc())
        .limit(10)
    )
    sintomas_rows = result.all()
    top_sintomas = [
        {"sintoma": row.sintoma, "frecuencia": row.frecuencia}
        for row in sintomas_rows
    ]
    
    # --- Resumen ejecutivo para auditoría ---
    return {
        "periodo": {
            "mes": mes,
            "anio": anio,
            "nombre_mes": fecha_inicio.strftime("%B %Y")
        },
        "resumen": {
            "total_casos": total_casos,
            "tasa_concordancia_ia": tasa_concordancia,
            "discrepancias": discrepancias,
            "coincidencias": coincidencias
        },
        "distribucion_urgencia": distribucion_urgencia,
        "tiempos_atencion": tiempos_por_nivel,
        "tendencia_diaria": tendencia_diaria,
        "top_sintomas": top_sintomas,
        "nota_anonimizacion": "Este reporte no contiene información personal identificable (PII) de pacientes.",
        "generado": datetime.now().isoformat()
    }