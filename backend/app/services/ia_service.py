import json
import time
import logging
from typing import Dict, Any, Optional, List
from datetime import datetime
from openai import AsyncOpenAI, APIError, RateLimitError
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.schemas.triaje import RespuestaLlamaJSON, SignosVitalesCreate, NivelUrgencia
from app.schemas.paciente import PacienteResponse
from app.models.resultado_ia import ResultadoIA
from app.models.triaje import Triaje

logger = logging.getLogger(__name__)

class IAService:
    """
    Servicio de integración con LLM para triaje clínico.
    Implementa ingeniería de prompts médicos con salida estructurada.
    """
    
    def __init__(self):
        self.api_key = settings.OPENAI_API_KEY
        self.model = settings.OPENAI_MODEL
        self.base_url = settings.OPENAI_BASE_URL
        
        # Validar API Key al iniciar (acepta OpenAI sk- o Groq gsk-)
        is_valid_key = self.api_key and (self.api_key.startswith("sk-") or self.api_key.startswith("gsk_"))
        
        if not is_valid_key:
            logger.error("=" * 60)
            logger.error("ERROR: API Key no configurada correctamente")
            logger.error(f"Valor actual: {'[VACIO]' if not self.api_key else self.api_key[:10] + '...'}")
            logger.error("Se requiere API Key valida (OpenAI: sk-xxx o Groq: gsk_xxx)")
            logger.error("=" * 60)
            self.client = None
        else:
            provider = "Groq" if self.base_url and "groq" in self.base_url else "OpenAI"
            logger.info(f"IAService inicializado con {provider} - Modelo: {self.model}")
            
            # Configurar cliente con base_url opcional (para Groq)
            client_kwargs = {"api_key": self.api_key}
            if self.base_url:
                client_kwargs["base_url"] = self.base_url
            
            self.client = AsyncOpenAI(**client_kwargs)
        
    async def evaluar_triaje(
        self,
        motivo_consulta: str,
        signos_vitales: SignosVitalesCreate,
        sintomas: List[Dict[str, str]],
        paciente: Optional[PacienteResponse] = None,
        antecedentes_hce: Optional[List[Dict]] = None
    ) -> tuple[RespuestaLlamaJSON, Dict[str, Any], float]:
        """
        Evalúa el caso clínico y retorna sugerencia de triaje.
        
        Returns:
            tuple: (respuesta_estructurada, metadata_raw, latencia_segundos)
        """
        # Verificar que el cliente esté inicializado
        if self.client is None:
            raise ValueError("OpenAI API Key no configurada. No se puede realizar evaluacion IA.")
        
        start_time = time.time()
        
        # Construir el prompt del sistema (System Prompt)
        system_prompt = self._build_system_prompt()
        
        # Construir el prompt del usuario (User Prompt) con contexto clínico
        user_prompt = self._build_user_prompt(
            motivo_consulta=motivo_consulta,
            signos_vitales=signos_vitales,
            sintomas=sintomas,
            paciente=paciente,
            antecedentes_hce=antecedentes_hce
        )
        
        # Log para auditoría (sin datos sensibles)
        logger.info(f"Enviando prompt a LLM: {user_prompt[:200]}...")
        
        try:
            # Llamada a OpenAI con Structured Outputs
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.1,  # Baja temperatura para consistencia clínica
                response_format={"type": "json_object"},
                timeout=30.0  # Timeout de 30 segundos
            )
            
            latency = time.time() - start_time
            
            # Extraer y parsear respuesta
            respuesta_raw = response.choices[0].message.content
            logger.debug(f"Respuesta raw del LLM: {respuesta_raw}")
            
            # Validar estructura con Pydantic
            respuesta_estructurada = self._validate_and_parse_response(respuesta_raw)
            
            # Preparar metadata
            metadata = {
                "modelo": self.model,
                "prompt_enviado": user_prompt,
                "system_prompt": system_prompt,
                "tokens_prompt": response.usage.prompt_tokens if response.usage else 0,
                "tokens_completion": response.usage.completion_tokens if response.usage else 0,
                "finish_reason": response.choices[0].finish_reason
            }
            
            return respuesta_estructurada, metadata, latency
            
        except APIError as e:
            logger.error(f"Error de API de OpenAI: {str(e)}")
            raise
        except RateLimitError as e:
            logger.error(f"Rate limit excedido: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Error inesperado en IA service: {str(e)}")
            raise
    
    def _build_system_prompt(self) -> str:
        """
        Construye el System Prompt con directivas médicas estrictas.
        Este prompt define el rol, restricciones y formato de salida.
        """
        return """# SISTEMA EXPERTO EN TRIAJE CLÍNICO (MANCHESTER Triage System)

## Rol
Eres un sistema de asistencia al triaje de enfermería, basado en el Protocolo Manchester. 
Tu función es **estratificar el riesgo** del paciente, no diagnosticar enfermedades específicas. 
Eres una herramienta de soporte decisional; la validación final es del profesional de salud.

## Restricciones CRÍTICAS
1. **RESPONDE ÚNICAMENTE con un objeto JSON válido**. Sin texto narrativo, sin explicaciones.
2. No emitas diagnósticos definitivos (ej. "Apendicitis") → usa términos sindrómicos: "Síndrome doloroso abdominal agudo".
3. Si falta información crítica, asume el peor escenario plausible dentro de la ética clínica.
4. Prioriza siempre la seguridad del paciente sobre la especificidad diagnóstica.

## Reglas Duras de Asignación de Nivel (No negociables)
- **RED (Crítico)**: 
  - Frecuencia cardíaca > 120 + disnea
  - Saturación O2 < 90% + dificultad respiratoria
  - Dolor torácico + diaforesis + disnea
  - Escala de coma < 9
  - Convulsión activa
  
- **ORANGE (Urgente)**:
  - Frecuencia cardíaca > 130 o < 50
  - Saturación O2 90-93%
  - Dolor severo (8-10/10)
  - Cefalea + déficit neurológico focal
  - Fiebre > 40°C en adulto

- **YELLOW (Poco urgente)**:
  - Fiebre 38-39.9°C
  - Dolor moderado (4-7/10)
  - Heridas que requieren sutura simple
  - Disnea de esfuerzo moderado

- **GREEN (No urgente)**:
  - Dolor leve (<4/10)
  - Síntomas gripales sin factores de riesgo
  - Consultas administrativas

- **BLUE (Consulta administrativa)**: 
  - Solicitud de certificados
  - Resultados de laboratorio normales

## Formato de Salida (JSON estricto)
{
  "nivel_urgencia": "RED|ORANGE|YELLOW|GREEN|BLUE",
  "diagnosticos": ["Síndrome X", "Síndrome Y"],
  "recomendaciones": "Conducta resumida en 1-2 líneas",
  "signos_alarma": ["signo1", "signo2"],
  "requiere_aislamiento": false
}

## Consideraciones Especiales
- Si el paciente es diabético o hipertenso, considera descompensación metabólica.
- Antecedentes de alergia grave: eleva nivel de urgencia un escalón.
- Pacientes > 65 años: umbral más bajo para clasificar como YELLOW/ORANGE.
- Nunca bajes el nivel por presión asistencial. La seguridad es primero.

Inicia tu respuesta con { y termina con }. Nada más."""
    
    def _build_user_prompt(
        self,
        motivo_consulta: str,
        signos_vitales: SignosVitalesCreate,
        sintomas: List[Dict[str, str]],
        paciente: Optional[PacienteResponse] = None,
        antecedentes_hce: Optional[List[Dict]] = None
    ) -> str:
        """
        Construye el User Prompt con el caso clínico específico.
        Incluye inyección condicional de antecedentes.
        """
        prompt_parts = []
        
        # 1. Datos demográficos (si disponibles)
        if paciente:
            edad = paciente.edad
            genero = paciente.genero or "No especificado"
            prompt_parts.append(f"## Datos del Paciente\n- Edad: {edad} años\n- Género: {genero}")
            
            # Factor de riesgo por edad
            if edad > 65:
                prompt_parts.append("- **Factor geriátrico**: Paciente >65 años, considerar mayor fragilidad.")
            elif edad < 5:
                prompt_parts.append("- **Factor pediátrico**: Paciente <5 años, considerar anatomía/ fisiología especial.")
        
        # 2. Antecedentes HCE (inyección condicional)
        if antecedentes_hce:
            alertas = []
            for ant in antecedentes_hce:
                if ant.get('tipo') == 'Alergia':
                    alertas.append(f"⚠️ Alergia: {ant.get('nombre')} - {ant.get('descripcion', '')}")
                elif ant.get('tipo') == 'Patologia':
                    alertas.append(f"📋 Patología base: {ant.get('nombre')}")
            
            if alertas:
                prompt_parts.append("\n## Antecedentes Clínicos Relevantes (HCE)")
                prompt_parts.extend(alertas)
                prompt_parts.append("\n**Considera estos antecedentes en tu evaluación.**")
        
        # 3. Motivo de consulta
        prompt_parts.append(f"\n## Motivo de Consulta\n{motivo_consulta}")
        
        # 4. Signos Vitales
        sv = signos_vitales
        sv_lines = []
        if sv.presion_sistolica and sv.presion_diastolica:
            sv_lines.append(f"- Presión arterial: {sv.presion_sistolica}/{sv.presion_diastolica} mmHg")
        if sv.frecuencia_cardiaca:
            sv_lines.append(f"- Frecuencia cardíaca: {sv.frecuencia_cardiaca} lpm")
        if sv.frecuencia_respiratoria:
            sv_lines.append(f"- Frecuencia respiratoria: {sv.frecuencia_respiratoria} rpm")
        if sv.temperatura:
            sv_lines.append(f"- Temperatura: {sv.temperatura}°C")
        if sv.saturacion_o2:
            sv_lines.append(f"- Saturación O2: {sv.saturacion_o2}%")
        
        if sv_lines:
            prompt_parts.append("\n## Signos Vitales")
            prompt_parts.extend(sv_lines)
        
        # 5. Síntomas
        if sintomas:
            sintomas_lines = ["\n## Síntomas Reportados"]
            for s in sintomas:
                intensidad = s.get('intensidad', 'No especificada')
                desc = s.get('descripcion_libre', '')
                sintomas_lines.append(f"- {s.get('sintoma')} (Intensidad: {intensidad}): {desc}")
            prompt_parts.extend(sintomas_lines)
        
        # 6. Instrucción final
        prompt_parts.append("\n## Instrucción\nEvalúa el caso según criterios Manchester y retorna SOLO el objeto JSON.")
        
        return "\n".join(prompt_parts)
    
    def _validate_and_parse_response(self, respuesta_raw: str) -> RespuestaLlamaJSON:
        """
        Valida la respuesta del LLM contra el esquema Pydantic.
        Si falla, intenta reparar respuestas comunes.
        """
        try:
            # Intentar parsear JSON
            data = json.loads(respuesta_raw)
            
            # Validar con Pydantic
            validated = RespuestaLlamaJSON(**data)
            return validated
            
        except json.JSONDecodeError as e:
            logger.error(f"JSON inválido del LLM: {respuesta_raw[:200]}")
            # Fallback: retornar nivel por defecto seguro
            return RespuestaLlamaJSON(
                nivel_urgencia=NivelUrgencia.YELLOW,
                diagnosticos=["Error en procesamiento de IA"],
                recomendaciones="Validación manual requerida por fallo técnico",
                signos_alarma=["Error de comunicación con sistema IA"],
                requiere_aislamiento=False
            )
        except Exception as e:
            logger.error(f"Error validando respuesta: {str(e)}")
            # Fallback seguro
            return RespuestaLlamaJSON(
                nivel_urgencia=NivelUrgencia.YELLOW,
                diagnosticos=["Error de validación"],
                recomendaciones="Proceder con triaje manual estándar",
                signos_alarma=[],
                requiere_aislamiento=False
            )
    
    async def guardar_resultado_ia(
        self,
        db: AsyncSession,
        triaje_id: int,
        respuesta: RespuestaLlamaJSON,
        metadata: Dict[str, Any],
        latencia: float
    ) -> ResultadoIA:
        """Persiste el resultado de IA en la base de datos"""
        resultado = ResultadoIA(
            triaje_id=triaje_id,
            prompt_enviado=metadata.get("prompt_enviado", ""),
            respuesta_raw_llm=json.dumps(respuesta.model_dump(), ensure_ascii=False),
            diagnosticos_json={
                "diagnosticos": respuesta.diagnosticos,
                "signos_alarma": respuesta.signos_alarma
            },
            recomendaciones_json={
                "recomendacion": respuesta.recomendaciones,
                "requiere_aislamiento": respuesta.requiere_aislamiento
            },
            modelo_utilizado=metadata.get("modelo", ""),
            latencia_segundos=latencia
        )
        db.add(resultado)
        await db.flush()
        return resultado


# Instancia global
ia_service = IAService()


async def get_ia_evaluation_or_503(
    motivo_consulta: str,
    signos_vitales: SignosVitalesCreate,
    sintomas: List[Dict[str, str]],
    paciente: Optional[PacienteResponse] = None,
    antecedentes_hce: Optional[List[Dict]] = None
) -> RespuestaLlamaJSON:
    """
    Wrapper que maneja errores de IA y retorna 503 si es necesario.
    Para ser usado desde los routers.
    """
    try:
        respuesta, metadata, latencia = await ia_service.evaluar_triaje(
            motivo_consulta=motivo_consulta,
            signos_vitales=signos_vitales,
            sintomas=sintomas,
            paciente=paciente,
            antecedentes_hce=antecedentes_hce
        )
        return respuesta
    except (APIError, RateLimitError, Exception) as e:
        logger.critical(f"Servicio IA no disponible: {str(e)}")
        # Relanzar para que el router capture y retorne 503
        raise ServiceUnavailableError("Servicio de asistencia IA no disponible. Proceda con triaje manual.")


class ServiceUnavailableError(Exception):
    """Excepción para cuando el LLM no responde correctamente"""
    pass