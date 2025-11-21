# 🤖 LinkedIn Chatbot - Publicador Inteligente

Sistema web completo para publicar en LinkedIn automáticamente con IA.

## ✨ Características

✅ **Chatbot Web Interactivo** - Interfaz conversacional  
✅ **Google Gemini IA** - Sugiere y mejora textos  
✅ **linkedin-api** - Publica automáticamente  
✅ **GitHub Storage** - Guarda fotos en repositorio  
✅ **Historial Completo** - Mantiene registro de posts  

## 🚀 Inicio Rápido

### 1. Instalar Dependencias

```bash
pip install -r requirements.txt
```

### 2. Configurar .env

Edita `c:\github\linkedin\.env` con tus datos:

```
LINKEDIN_EMAIL=job.llanos@gmail.com
LINKEDIN_PASSWORD=Tito#2008
GEMINI_API_KEY=tu_api_key_aqui
GITHUB_TOKEN=tu_token_aqui
```

### 3. Obtener API Keys

**Google Gemini:**
1. Ve a https://aistudio.google.com/app/apikey
2. Crea una nueva API Key
3. Cópiala en .env

**GitHub Token:**
1. Ve a https://github.com/settings/tokens
2. Click "Generate new token"
3. Selecciona permisos de "repo"
4. Cópialo en .env

### 4. Ejecutar Backend

```bash
cd backend
python app.py
```

Verás:
```
🚀 Servidor ejecutando en http://localhost:5000
```

### 5. Abrir Frontend

```bash
Abre frontend/index.html en tu navegador
```

## 📁 Estructura

```
linkedin/
├── backend/
│   ├── app.py              # Servidor Flask
│   ├── linkedin_handler.py # Publicar en LinkedIn
│   ├── gemini_handler.py   # Generar con IA
│   ├── github_handler.py   # Guardar fotos
│   └── requirements.txt
├── frontend/
│   ├── index.html          # Chatbot web
│   ├── style.css           # Estilos
│   └── script.js           # Lógica
├── fotos/                  # Carpeta de imágenes
├── .env                    # Credenciales (SECRETO)
└── historico.json          # Historial de posts
```

## 🎯 Cómo Usar

### 1. Publicar Ahora
- Click "Publicar"
- Escribe tu mensaje
- Adjunta foto (opcional)
- Puedes mejorar con IA
- Click "Publicar"

### 2. Generar Sugerencia
- Click "Sugerir"
- Describe el tema
- Elige tono (profesional, casual, etc)
- Recibe sugerencia con IA
- Cópialo o edítalo

### 3. Ver Historial
- Click "Historial"
- Ves los últimos 5 posts publicados

## 🔑 API Endpoints

| Endpoint | Método | Descripción |
|----------|--------|-------------|
| `/api/health` | GET | Verificar servidor |
| `/api/chat` | POST | Chat con IA |
| `/api/sugerir` | POST | Generar sugerencia |
| `/api/mejorar` | POST | Mejorar texto |
| `/api/publicar` | POST | Publicar en LinkedIn |
| `/api/subir-foto` | POST | Subir foto a GitHub |
| `/api/historial` | GET | Ver historial |
| `/api/fotos` | GET | Ver fotos en GitHub |

## ⚠️ Importante

- **No pushees .env a GitHub** (contiene credenciales)
- **Máximo 5-10 posts/día** (LinkedIn detecta bots)
- **Las fotos se guardan en GitHub automáticamente**
- **El historial se actualiza en tiempo real**

## 🐛 Troubleshooting

**Error: "Connection refused"**
- Asegúrate que el backend está ejecutándose
- Verifica que el puerto 5000 está disponible

**Error: "API Key inválida"**
- Verifica tu Google Gemini API Key en .env
- Crea una nueva en https://aistudio.google.com/app/apikey

**Error: "No puedo conectar a LinkedIn"**
- Verifica email y contraseña en .env
- Asegúrate de que 2FA no está habilitado

## 📝 Notas

- El sistema usa `linkedin-api` que simula un navegador
- No es oficial pero funciona y es gratis
- LinkedIn puede cambiar su código en cualquier momento
- Usa responsablemente, no publiques spam

## 🔗 Enlaces

- Perfil LinkedIn: https://www.linkedin.com/in/job-llanos-b151574b/
- GitHub: https://github.com/Trimpulso/linkedin
- Google Gemini: https://aistudio.google.com

---

**Versión:** 1.0  
**Fecha:** Noviembre 2025  
**Autor:** LinkedIn Chatbot
