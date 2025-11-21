"""
Backend Flask - LinkedIn Chatbot
API REST para el chatbot web
"""

import logging
import os
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv
from pathlib import Path
import json

# Importar handlers
from linkedin_handler import LinkedInHandler
from gemini_handler import GeminiHandler
from github_handler import GitHubHandler

# Cargar variables de entorno
load_dotenv()

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Crear app Flask
app = Flask(__name__, static_folder='../frontend', static_url_path='/frontend')
CORS(app)

# Inicializar handlers globales
linkedin = None
gemini = None
github = None

def inicializar_handlers():
    """Inicializar todos los handlers"""
    global linkedin, gemini, github
    
    try:
        # LinkedIn
        try:
            linkedin = LinkedInHandler(
                os.getenv('LINKEDIN_EMAIL'),
                os.getenv('LINKEDIN_PASSWORD')
            )
            logger.info("✅ LinkedIn handler inicializado")
        except Exception as e:
            logger.warning(f"⚠️ LinkedIn no disponible: {str(e)}")
            linkedin = None
        
        # Gemini
        try:
            gemini = GeminiHandler(os.getenv('GEMINI_API_KEY'))
            logger.info("✅ Gemini handler inicializado")
        except Exception as e:
            logger.error(f"❌ Error en Gemini: {str(e)}")
            return False
        
        # GitHub
        try:
            github = GitHubHandler(
                os.getenv('GITHUB_TOKEN'),
                os.getenv('GITHUB_OWNER'),
                os.getenv('GITHUB_REPO')
            )
            logger.info("✅ GitHub handler inicializado")
        except Exception as e:
            logger.warning(f"⚠️ GitHub no disponible: {str(e)}")
            github = None
        
        logger.info("✅ Sistema inicializado (parcialmente)")
        return True
    
    except Exception as e:
        logger.error(f"❌ Error crítico al inicializar: {str(e)}")
        return False


# RUTAS API

@app.route('/', methods=['GET'])
def index():
    """Redirigir a la página principal"""
    return send_from_directory('../frontend', 'index.html')

@app.route('/api/health', methods=['GET'])
def health():
    """Verificar que el servidor está funcionando"""
    return jsonify({"status": "ok", "message": "Servidor funcionando"})


@app.route('/api/status', methods=['GET'])
def status():
    """Obtener estado del sistema"""
    return jsonify({
        "linkedin": linkedin is not None,
        "gemini": gemini is not None,
        "github": github is not None,
        "timestamp": str(Path(__file__).parent.parent / "historico.json")
    })


@app.route('/api/chat', methods=['POST'])
def chat():
    """Chat conversacional con IA"""
    try:
        data = request.json
        mensaje = data.get('mensaje', '')
        
        if not mensaje:
            return jsonify({"error": "Mensaje vacío"}), 400
        
        respuesta = gemini.chat_conversacional(mensaje)
        
        return jsonify({
            "success": True,
            "respuesta": respuesta,
            "tipo": "chat"
        })
    
    except Exception as e:
        logger.error(f"Error en chat: {str(e)}")
        return jsonify({"error": str(e)}), 500


@app.route('/api/sugerir', methods=['POST'])
def sugerir():
    """Generar sugerencia de post con IA"""
    try:
        data = request.json
        tema = data.get('tema', '')
        tono = data.get('tono', 'profesional')
        
        if not tema:
            return jsonify({"error": "Tema requerido"}), 400
        
        sugerencia = gemini.generar_sugerencia(tema, tono)
        
        return jsonify({
            "success": True,
            "sugerencia": sugerencia,
            "tipo": "sugerencia"
        })
    
    except Exception as e:
        logger.error(f"Error al sugerir: {str(e)}")
        return jsonify({"error": str(e)}), 500


@app.route('/api/mejorar', methods=['POST'])
def mejorar():
    """Mejorar un texto con IA"""
    try:
        data = request.json
        texto = data.get('texto', '')
        tono = data.get('tono', 'profesional')
        
        if not texto:
            return jsonify({"error": "Texto requerido"}), 400
        
        texto_mejorado = gemini.mejorar_texto(texto, tono)
        hashtags = gemini.generar_hashtags(texto_mejorado)
        
        return jsonify({
            "success": True,
            "texto_original": texto,
            "texto_mejorado": texto_mejorado,
            "hashtags": hashtags
        })
    
    except Exception as e:
        logger.error(f"Error al mejorar: {str(e)}")
        return jsonify({"error": str(e)}), 500


@app.route('/api/publicar', methods=['POST'])
def publicar():
    """Publicar en LinkedIn"""
    try:
        data = request.json
        texto = data.get('texto', '')
        imagen_url = data.get('imagen_url')
        
        if not texto:
            return jsonify({"error": "Texto requerido"}), 400
        
        if not linkedin:
            return jsonify({
                "success": True,
                "message": "Post guardado localmente (LinkedIn no disponible)",
                "advertencia": "Necesitas resolver el desafío de LinkedIn para publicar directamente",
                "texto": texto
            })
        
        # Publicar
        resultado = linkedin.publicar_post(texto, imagen_url)
        
        return jsonify(resultado)
    
    except Exception as e:
        logger.error(f"Error al publicar: {str(e)}")
        return jsonify({"error": str(e)}), 500


@app.route('/api/subir-foto', methods=['POST'])
def subir_foto():
    """Subir foto a GitHub"""
    try:
        if 'file' not in request.files:
            return jsonify({"error": "No file provided"}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({"error": "No selected file"}), 400
        
        # Guardar temporalmente
        temp_path = f"/tmp/{file.filename}"
        file.save(temp_path)
        
        # Subir a GitHub
        resultado = github.subir_foto(temp_path, file.filename)
        
        # Eliminar archivo temporal
        Path(temp_path).unlink(missing_ok=True)
        
        return jsonify(resultado)
    
    except Exception as e:
        logger.error(f"Error al subir foto: {str(e)}")
        return jsonify({"error": str(e)}), 500


@app.route('/api/historial', methods=['GET'])
def historial():
    """Obtener historial de posts"""
    try:
        if not linkedin:
            return jsonify({"success": True, "historial": [], "total": 0})
        
        resultado = linkedin.obtener_historial()
        return jsonify({
            "success": True,
            "historial": resultado,
            "total": len(resultado)
        })
    
    except Exception as e:
        logger.error(f"Error al obtener historial: {str(e)}")
        return jsonify({"error": str(e)}), 500


@app.route('/api/fotos', methods=['GET'])
def fotos():
    """Obtener lista de fotos en GitHub"""
    try:
        if not github:
            return jsonify({"success": True, "fotos": [], "total": 0})
        
        fotos_list = github.listar_fotos()
        return jsonify({
            "success": True,
            "fotos": fotos_list,
            "total": len(fotos_list)
        })
    
    except Exception as e:
        logger.error(f"Error al obtener fotos: {str(e)}")
        return jsonify({"error": str(e)}), 500


# MAIN
if __name__ == '__main__':
    print("\n" + "="*70)
    print("  🤖 LINKEDIN CHATBOT - Backend")
    print("="*70)
    
    # Inicializar
    print("\n⏳ Inicializando handlers...")
    inicializar_handlers()
    print("✅ Sistema listo (algunos servicios pueden estar en modo degradado)\n")
    
    puerto = int(os.getenv('FLASK_PORT', 5000))
    print(f"🚀 Servidor ejecutando en http://localhost:{puerto}")
    print("📡 Chat disponible")
    print("="*70 + "\n")
    
    app.run(
        host='0.0.0.0',
        port=puerto,
        debug=os.getenv('FLASK_ENV') == 'development'
    )
