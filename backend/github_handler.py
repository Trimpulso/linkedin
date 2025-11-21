"""
Handler para subir fotos a GitHub
"""

import logging
import base64
from pathlib import Path
from github import Github
from datetime import datetime

logger = logging.getLogger(__name__)


class GitHubHandler:
    """Maneja subida de fotos a GitHub"""
    
    def __init__(self, token: str, owner: str, repo: str):
        """
        Inicializar GitHub handler
        
        Args:
            token: Token personal de GitHub
            owner: Propietario del repositorio
            repo: Nombre del repositorio
        """
        self.token = token
        self.owner = owner
        self.repo = repo
        self.github = None
        self.repository = None
        self.conectar()
    
    def conectar(self):
        """Conectarse a GitHub"""
        try:
            self.github = Github(self.token)
            self.repository = self.github.get_user(self.owner).get_repo(self.repo)
            logger.info(f"✅ Conectado a GitHub: {self.owner}/{self.repo}")
        except Exception as e:
            logger.error(f"❌ Error al conectar a GitHub: {str(e)}")
            raise
    
    def subir_foto(self, ruta_local: str, nombre_en_github: str = None) -> dict:
        """
        Subir foto a GitHub
        
        Args:
            ruta_local: Ruta local de la foto
            nombre_en_github: Nombre en GitHub (si no se especifica, se usa el original)
        
        Returns:
            dict con información del archivo subido
        """
        try:
            ruta = Path(ruta_local)
            
            if not ruta.exists():
                return {
                    "success": False,
                    "error": "Archivo no encontrado"
                }
            
            # Usar nombre original si no se especifica
            if not nombre_en_github:
                nombre_en_github = ruta.name
            
            # Ruta en GitHub (carpeta fotos)
            github_path = f"fotos/{datetime.now().strftime('%Y%m%d')}_{nombre_en_github}"
            
            # Leer archivo
            with open(ruta, 'rb') as f:
                contenido = f.read()
            
            # Convertir a base64
            contenido_base64 = base64.b64encode(contenido).decode()
            
            logger.info(f"Subiendo {nombre_en_github} a {github_path}...")
            
            # Subir a GitHub
            self.repository.create_file(
                path=github_path,
                message=f"Agregar foto: {nombre_en_github}",
                content=contenido_base64,
                branch="main"
            )
            
            # Construir URL pública
            url_publica = f"https://raw.githubusercontent.com/{self.owner}/{self.repo}/main/{github_path}"
            
            logger.info(f"✅ Foto subida: {url_publica}")
            
            return {
                "success": True,
                "github_path": github_path,
                "url": url_publica,
                "filename": nombre_en_github,
                "timestamp": datetime.now().isoformat()
            }
        
        except Exception as e:
            logger.error(f"❌ Error al subir foto: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def listar_fotos(self) -> list:
        """Listar todas las fotos en GitHub"""
        try:
            fotos = []
            contents = self.repository.get_contents("fotos")
            
            for content in contents:
                if content.type == "file":
                    fotos.append({
                        "nombre": content.name,
                        "url": content.download_url,
                        "path": content.path
                    })
            
            logger.info(f"✅ {len(fotos)} fotos encontradas en GitHub")
            return fotos
        
        except Exception as e:
            logger.warning(f"⚠️ No hay fotos en GitHub aún: {str(e)}")
            return []
    
    def guardar_historial(self, historial_json: str) -> dict:
        """
        Guardar historial en GitHub
        
        Args:
            historial_json: String JSON del historial
        
        Returns:
            Resultado de la operación
        """
        try:
            github_path = "historico.json"
            
            logger.info("Guardando historial en GitHub...")
            
            self.repository.create_file(
                path=github_path,
                message=f"Actualizar historial: {datetime.now().isoformat()}",
                content=historial_json,
                branch="main"
            )
            
            logger.info("✅ Historial guardado en GitHub")
            return {
                "success": True,
                "path": github_path,
                "timestamp": datetime.now().isoformat()
            }
        
        except Exception as e:
            logger.error(f"❌ Error al guardar historial: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }
