"""
Handler para integrar Google Gemini IA
"""

import logging
import google.generativeai as genai
from typing import Optional

logger = logging.getLogger(__name__)


class GeminiHandler:
    """Maneja todas las operaciones con Google Gemini IA"""
    
    def __init__(self, api_key: str):
        """
        Inicializar Gemini
        
        Args:
            api_key: API Key de Google Gemini
        """
        self.api_key = api_key
        self.modelo = None
        self.configurar()
    
    def configurar(self):
        """Configurar Gemini"""
        try:
            genai.configure(api_key=self.api_key)
            self.modelo = genai.GenerativeModel('gemini-pro')
            logger.info("✅ Gemini configurado exitosamente")
        except Exception as e:
            logger.error(f"❌ Error al configurar Gemini: {str(e)}")
            raise
    
    def mejorar_texto(self, texto: str, tono: str = "profesional") -> str:
        """
        Mejorar un texto usando IA
        
        Args:
            texto: Texto a mejorar
            tono: Tono deseado (profesional, casual, inspirador, educativo)
        
        Returns:
            Texto mejorado
        """
        try:
            prompt = f"""
            Mejora este texto para LinkedIn. Manten el mensaje original pero hazlo más atractivo.
            Tono: {tono}
            
            Texto original:
            {texto}
            
            Por favor, solo devuelve el texto mejorado sin explicaciones adicionales.
            Máximo 3000 caracteres.
            """
            
            respuesta = self.modelo.generate_content(prompt)
            texto_mejorado = respuesta.text.strip()
            
            logger.info("✅ Texto mejorado con IA")
            return texto_mejorado
        
        except Exception as e:
            logger.error(f"❌ Error al mejorar texto: {str(e)}")
            return texto
    
    def generar_sugerencia(self, tema: str, tono: str = "profesional", incluir_hashtags: bool = True) -> str:
        """
        Generar un post completo basado en un tema
        
        Args:
            tema: Tema del post
            tono: Tono deseado
            incluir_hashtags: Si incluir hashtags
        
        Returns:
            Post generado
        """
        try:
            prompt = f"""
            Crea un post corto y atractivo para LinkedIn.
            
            Tema: {tema}
            Tono: {tono}
            Incluir hashtags: {incluir_hashtags}
            
            Requisitos:
            - Máximo 500 caracteres
            - Atractivo y profesional
            - Incluir emojis relevantes
            {f"- Incluir 3-5 hashtags relevantes" if incluir_hashtags else ""}
            
            Solo devuelve el post, sin explicaciones.
            """
            
            respuesta = self.modelo.generate_content(prompt)
            post = respuesta.text.strip()
            
            logger.info("✅ Post generado con IA")
            return post
        
        except Exception as e:
            logger.error(f"❌ Error al generar sugerencia: {str(e)}")
            return f"Post sobre: {tema}"
    
    def generar_hashtags(self, texto: str) -> list:
        """
        Generar hashtags sugeridos basado en el texto
        
        Args:
            texto: Texto para analizar
        
        Returns:
            Lista de hashtags sugeridos
        """
        try:
            prompt = f"""
            Analiza este texto y sugerira 5-8 hashtags relevantes para LinkedIn.
            
            Texto:
            {texto}
            
            Devuelve solo los hashtags separados por comas, sin explicaciones.
            Formato: #hashtag1, #hashtag2, #hashtag3...
            """
            
            respuesta = self.modelo.generate_content(prompt)
            hashtags_str = respuesta.text.strip()
            hashtags = [h.strip() for h in hashtags_str.split(',')]
            
            logger.info(f"✅ {len(hashtags)} hashtags generados")
            return hashtags
        
        except Exception as e:
            logger.error(f"❌ Error al generar hashtags: {str(e)}")
            return []
    
    def chat_conversacional(self, mensaje: str, contexto: Optional[str] = None) -> str:
        """
        Chat conversacional con IA
        
        Args:
            mensaje: Mensaje del usuario
            contexto: Contexto anterior (opcional)
        
        Returns:
            Respuesta de IA
        """
        try:
            prompt = mensaje
            if contexto:
                prompt = f"{contexto}\n\nNuevo mensaje: {mensaje}"
            
            respuesta = self.modelo.generate_content(prompt)
            return respuesta.text.strip()
        
        except Exception as e:
            logger.error(f"❌ Error en chat: {str(e)}")
            return "Lo siento, hubo un error procesando tu mensaje."
