"""
Servicio para procesar transcripciones con OpenAI.
Extrae requerimientos, fases del proyecto y documentación.
"""
from typing import Dict, Any, List, Optional
from openai import AsyncOpenAI
import json
from app.core.config import settings


class OpenAIService:
    """Servicio para integración con OpenAI"""
    
    def __init__(self):
        # Inicialización opcional - no falla si no hay API key
        self.api_key = settings.OPENAI_API_KEY if hasattr(settings, 'OPENAI_API_KEY') else None
        self.client = None
        self.model = getattr(settings, 'OPENAI_MODEL', 'gpt-4-turbo-preview')
        
        # Solo inicializar cliente si hay API key válida
        if self.api_key and self.api_key != "tu-api-key-aqui":
            try:
                self.client = AsyncOpenAI(api_key=self.api_key)
            except Exception as e:
                print(f"⚠️  Warning: No se pudo inicializar OpenAI client: {e}")
                self.client = None
        else:
            print("⚠️  Warning: OpenAI API key no configurada. El procesamiento con IA no estará disponible.")
    
    async def analyze_transcription(
        self, 
        transcription_text: str,
        project_context: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Analiza una transcripción y extrae:
        - Resumen ejecutivo
        - Fases del proyecto identificadas
        - Requerimientos funcionales y no funcionales
        - Documentación técnica
        """
        
        # Verificar si el cliente está disponible
        if not self.client:
            raise Exception(
                "OpenAI API key no configurada. "
                "Por favor configura OPENAI_API_KEY en el archivo .env para usar esta funcionalidad."
            )
        
        system_prompt = self._build_system_prompt()
        user_prompt = self._build_user_prompt(transcription_text, project_context)
        
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.3,  # Baja temperatura para respuestas más determinísticas
                response_format={"type": "json_object"}
            )
            
            result = json.loads(response.choices[0].message.content)
            
            # Validar estructura
            return self._validate_and_normalize_response(result)
            
        except Exception as e:
            raise Exception(f"Error al procesar con OpenAI: {str(e)}")
    
    def _build_system_prompt(self) -> str:
        """Construye el prompt del sistema con instrucciones detalladas"""
        return """Eres un analista de software experto especializado en extraer información de reuniones de desarrollo.

Tu tarea es analizar transcripciones de reuniones de Microsoft Teams y extraer:

1. **Resumen Ejecutivo**: Un resumen conciso de los puntos principales discutidos
2. **Fases del Proyecto**: Las etapas generales identificadas (ej: Análisis, Diseño, Desarrollo, Testing, Despliegue)
3. **Requerimientos**: Funcionales, no funcionales y técnicos mencionados
4. **Decisiones Técnicas**: Tecnologías, arquitecturas, patrones discutidos
5. **Acciones Pendientes**: Tareas o temas que requieren seguimiento

**IMPORTANTE**: 
- Extrae SOLO información que esté EXPLÍCITAMENTE mencionada en la transcripción
- No inventes ni asumas información que no esté en el texto
- Clasifica los requerimientos por prioridad basándote en el tono y contexto de la conversación
- Identifica qué fase corresponde a cada requerimiento

Devuelve la respuesta en formato JSON con esta estructura exacta:

```json
{
  "summary": "Resumen ejecutivo breve",
  "phases": [
    {
      "name": "Nombre de la fase",
      "description": "Descripción detallada",
      "order": 1,
      "estimated_duration": "2 semanas"
    }
  ],
  "requirements": [
    {
      "title": "Título del requerimiento",
      "description": "Descripción detallada",
      "type": "functional|non_functional|technical|business",
      "priority": "low|medium|high|critical",
      "phase": "Nombre de la fase asociada"
    }
  ],
  "technical_decisions": [
    {
      "topic": "Tema decidido",
      "decision": "Decisión tomada",
      "rationale": "Justificación"
    }
  ],
  "action_items": [
    {
      "task": "Descripción de la tarea",
      "assigned_to": "Persona asignada (si se menciona)",
      "deadline": "Fecha límite (si se menciona)"
    }
  ]
}
```"""
    
    def _build_user_prompt(
        self, 
        transcription_text: str,
        project_context: Optional[str] = None
    ) -> str:
        """Construye el prompt del usuario con el contexto"""
        
        prompt = "Analiza la siguiente transcripción de reunión:\n\n"
        prompt += "=" * 80 + "\n"
        prompt += transcription_text
        prompt += "\n" + "=" * 80 + "\n\n"
        
        if project_context:
            prompt += f"**Contexto del proyecto:**\n{project_context}\n\n"
        
        prompt += "Extrae y estructura toda la información relevante siguiendo el formato JSON especificado."
        
        return prompt
    
    def _validate_and_normalize_response(self, response: Dict[str, Any]) -> Dict[str, Any]:
        """Valida y normaliza la respuesta de OpenAI"""
        
        # Estructura base
        normalized = {
            "summary": response.get("summary", ""),
            "phases": [],
            "requirements": [],
            "technical_decisions": response.get("technical_decisions", []),
            "action_items": response.get("action_items", [])
        }
        
        # Normalizar fases
        for phase in response.get("phases", []):
            normalized["phases"].append({
                "name": phase.get("name", ""),
                "description": phase.get("description", ""),
                "order": phase.get("order", 1),
                "estimated_duration": phase.get("estimated_duration")
            })
        
        # Normalizar requerimientos
        for req in response.get("requirements", []):
            normalized["requirements"].append({
                "title": req.get("title", ""),
                "description": req.get("description", ""),
                "type": req.get("type", "functional"),
                "priority": req.get("priority", "medium"),
                "phase": req.get("phase", "")
            })
        
        return normalized


# Instancia singleton
openai_service = OpenAIService()
