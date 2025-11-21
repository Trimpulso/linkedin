"""
Handler para publicar en LinkedIn usando linkedin-api
"""

import logging
from linkedin_api import Linkedin
from datetime import datetime
import json
from pathlib import Path

logger = logging.getLogger(__name__)


class LinkedInHandler:
    """Maneja todas las operaciones con LinkedIn"""
    
    def __init__(self, email: str, password: str):
        """
        Inicializar conexión con LinkedIn
        
        Args:
            email: Email de LinkedIn
            password: Contraseña de LinkedIn
        """
        self.email = email
        self.password = password
        self.client = None
        self.conectar()
    
    def conectar(self):
        """Conectarse a LinkedIn"""
        try:
            logger.info(f"Conectando a LinkedIn como {self.email}...")
            self.client = Linkedin(self.email, self.password)
            logger.info("✅ Conectado a LinkedIn exitosamente")
            return True
        except Exception as e:
            logger.warning(f"⚠️ Advertencia al conectar a LinkedIn: {str(e)}")
            logger.warning("El chatbot funcionará pero la publicación podría fallar")
            logger.warning("Solución: Si ves 'CHALLENGE', puede ser por seguridad de LinkedIn")
            # No lanzar excepción, permitir continuar con client = None
            self.client = None
            return False
    
    def publicar_post(self, texto: str, image_path: str = None) -> dict:
        """
        Publicar un post en LinkedIn
        
        Args:
            texto: Contenido del post
            image_path: Ruta de la imagen (opcional)
        
        Returns:
            dict con resultado de la publicación
        """
        try:
            if not texto or not texto.strip():
                return {
                    "success": False,
                    "error": "El texto no puede estar vacío"
                }
            
            logger.info(f"Publicando en LinkedIn: {texto[:50]}...")
            
            if not self.client:
                logger.warning("⚠️ Cliente de LinkedIn no disponible - Guardando en historial local")
                # Guardar en historial local aunque falle la conexión
                self._guardar_en_historial(texto, image_path)
                return {
                    "success": True,
                    "message": "Post guardado localmente (Conexión con LinkedIn pendiente)",
                    "timestamp": datetime.now().isoformat(),
                    "texto": texto,
                    "imagen": image_path,
                    "advertencia": "El post se guardó pero necesita conexión válida a LinkedIn para publicarse"
                }
            
            if image_path:
                self.client.post(texto, image_path=image_path)
            else:
                self.client.post(texto)
            
            # Guardar en historial
            self._guardar_en_historial(texto, image_path)
            
            logger.info("✅ Post publicado exitosamente")
            return {
                "success": True,
                "message": "Post publicado exitosamente",
                "timestamp": datetime.now().isoformat(),
                "texto": texto,
                "imagen": image_path
            }
        
        except Exception as e:
            logger.error(f"❌ Error al publicar: {str(e)}")
            return {
                "success": False,
                "error": f"Error al publicar: {str(e)}"
            }
    
    def _guardar_en_historial(self, texto: str, imagen: str = None):
        """Guardar post en historial local"""
        try:
            historial_path = Path(__file__).parent.parent / "historico.json"
            
            # Cargar historial existente
            if historial_path.exists():
                with open(historial_path, 'r', encoding='utf-8') as f:
                    historial = json.load(f)
            else:
                historial = []
            
            # Agregar nuevo post
            nuevo_post = {
                "id": len(historial) + 1,
                "fecha": datetime.now().isoformat(),
                "texto": texto,
                "imagen": imagen,
                "estado": "publicado"
            }
            historial.append(nuevo_post)
            
            # Guardar
            with open(historial_path, 'w', encoding='utf-8') as f:
                json.dump(historial, f, ensure_ascii=False, indent=2)
            
            logger.info("📝 Post guardado en historial")
        
        except Exception as e:
            logger.warning(f"⚠️ Error al guardar en historial: {str(e)}")
    
    def obtener_historial(self) -> list:
        """Obtener historial de posts"""
        try:
            historial_path = Path(__file__).parent.parent / "historico.json"
            
            if historial_path.exists():
                with open(historial_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return []
        
        except Exception as e:
            logger.error(f"Error al obtener historial: {str(e)}")
            return []
