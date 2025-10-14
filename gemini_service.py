"""
Servicio para integración con Google Gemini AI
Genera preguntas dinámicas y evalúa respuestas
"""

import os
import json
import google.generativeai as genai
from typing import List, Dict, Any

class GeminiService:
    def __init__(self):
        """Inicializa el servicio de Gemini"""
        self.api_key = os.getenv('GEMINI_API_KEY')
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY no está configurada en las variables de entorno")
        
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('gemini-pro')
    
    def generar_preguntas(self, tema: str, cantidad: int = 10) -> List[Dict[str, Any]]:
        """
        Genera preguntas dinámicas sobre un tema específico
        
        Args:
            tema: El tema de estudio
            cantidad: Número de preguntas a generar
            
        Returns:
            Lista de diccionarios con preguntas, opciones, respuestas correctas y explicaciones
        """
        prompt = f"""
        Genera {cantidad} preguntas educativas sobre el tema: "{tema}"
        
        Los tipos de preguntas deben ser variados:
        - Opción múltiple (4 opciones A, B, C, D)
        - Verdadero/Falso
        - Respuesta abierta (para explicaciones conceptuales)
        
        Responde ÚNICAMENTE en formato JSON válido con esta estructura:
        [
            {{
                "id": 1,
                "tipo": "opcion_multiple",
                "pregunta": "¿Cuál es la definición de...?",
                "opciones": {{
                    "A": "Opción A",
                    "B": "Opción B", 
                    "C": "Opción C",
                    "D": "Opción D"
                }},
                "respuesta_correcta": "A",
                "explicacion": "Explicación detallada de por qué esta es la respuesta correcta"
            }},
            {{
                "id": 2,
                "tipo": "verdadero_falso",
                "pregunta": "Afirmación sobre el tema...",
                "opciones": {{
                    "A": "Verdadero",
                    "B": "Falso"
                }},
                "respuesta_correcta": "A",
                "explicacion": "Explicación de por qué es verdadero/falso"
            }},
            {{
                "id": 3,
                "tipo": "respuesta_abierta",
                "pregunta": "Explica el concepto de...",
                "opciones": null,
                "respuesta_correcta": "Conceptos clave que debe incluir la respuesta",
                "explicacion": "Explicación detallada del concepto"
            }}
        ]
        
        IMPORTANTE:
        - Las preguntas deben ser apropiadas para nivel universitario
        - Incluye conceptos fundamentales del tema
        - Las explicaciones deben ser educativas y claras
        - No incluyas texto adicional fuera del JSON
        """
        
        try:
            response = self.model.generate_content(prompt)
            # Limpiar la respuesta para extraer solo el JSON
            content = response.text.strip()
            
            # Buscar el JSON en la respuesta
            if content.startswith('```json'):
                content = content[7:]
            if content.endswith('```'):
                content = content[:-3]
            
            preguntas = json.loads(content)
            return preguntas
            
        except Exception as e:
            print(f"Error generando preguntas: {e}")
            # Preguntas de fallback en caso de error
            return self._preguntas_fallback(tema, cantidad)
    
    def evaluar_respuesta(self, pregunta: Dict[str, Any], respuesta_usuario: str) -> Dict[str, Any]:
        """
        Evalúa la respuesta del usuario usando Gemini
        
        Args:
            pregunta: Diccionario con la pregunta original
            respuesta_usuario: Respuesta proporcionada por el usuario
            
        Returns:
            Diccionario con el resultado de la evaluación
        """
        if pregunta["tipo"] == "opcion_multiple" or pregunta["tipo"] == "verdadero_falso":
            # Para opciones múltiples y V/F, comparación directa
            es_correcta = respuesta_usuario.strip().upper() == pregunta["respuesta_correcta"].strip().upper()
            return {
                "correcta": es_correcta,
                "puntaje": 1 if es_correcta else 0,
                "explicacion": pregunta["explicacion"]
            }
        
        elif pregunta["tipo"] == "respuesta_abierta":
            # Para respuestas abiertas, usar Gemini para evaluar
            prompt = f"""
            Evalúa la siguiente respuesta a una pregunta educativa:
            
            PREGUNTA: {pregunta['pregunta']}
            RESPUESTA CORRECTA ESPERADA: {pregunta['respuesta_correcta']}
            RESPUESTA DEL USUARIO: {respuesta_usuario}
            
            Evalúa la respuesta del usuario considerando:
            1. Precisión conceptual
            2. Completitud de la respuesta
            3. Uso de terminología apropiada
            
            Responde ÚNICAMENTE en formato JSON:
            {{
                "correcta": true/false,
                "puntaje": 0.0-1.0,
                "explicacion": "Explicación detallada de la evaluación"
            }}
            """
            
            try:
                response = self.model.generate_content(prompt)
                content = response.text.strip()
                
                # Limpiar la respuesta
                if content.startswith('```json'):
                    content = content[7:]
                if content.endswith('```'):
                    content = content[:-3]
                
                evaluacion = json.loads(content)
                return evaluacion
                
            except Exception as e:
                print(f"Error evaluando respuesta: {e}")
                return {
                    "correcta": False,
                    "puntaje": 0,
                    "explicacion": "Error en la evaluación automática"
                }
    
    def _preguntas_fallback(self, tema: str, cantidad: int) -> List[Dict[str, Any]]:
        """Preguntas de fallback en caso de error con Gemini"""
        return [
            {
                "id": 1,
                "tipo": "opcion_multiple",
                "pregunta": f"¿Cuál es el concepto principal de {tema}?",
                "opciones": {
                    "A": "Concepto A",
                    "B": "Concepto B",
                    "C": "Concepto C", 
                    "D": "Concepto D"
                },
                "respuesta_correcta": "A",
                "explicacion": "Esta es una pregunta de ejemplo. Configura GEMINI_API_KEY para preguntas dinámicas."
            }
        ]
