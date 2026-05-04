import httpx
from app.config import settings
import logging

logger = logging.getLogger(__name__)

async def send_critical_alert(triaje_id: int, paciente_nombre: str, nivel_urgencia: str, motivo: str):
    """Envía webhook a n8n para alerta crítica"""
    try:
        async with httpx.AsyncClient() as client:
            payload = {
                "triaje_id": triaje_id,
                "paciente": paciente_nombre,
                "nivel_urgencia": nivel_urgencia,
                "motivo": motivo[:200],
                "timestamp": "now"
            }
            response = await client.post(
                settings.N8N_WEBHOOK_CRITICAL_ALERT,
                json=payload,
                timeout=5.0
            )
            if response.status_code == 200:
                logger.info(f"Alerta crítica enviada para triaje {triaje_id}")
            else:
                logger.error(f"Error enviando alerta: {response.status_code}")
    except Exception as e:
        logger.error(f"Error en webhook: {str(e)}")