@echo off
REM Script para ejecutar LinkedIn Chatbot en Windows

echo.
echo ╔════════════════════════════════════════════════════════╗
echo ║                                                        ║
echo ║   🤖 LINKEDIN CHATBOT - Iniciando Sistema...          ║
echo ║                                                        ║
echo ╚════════════════════════════════════════════════════════╝
echo.

REM Verificar si Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python no está instalado
    echo Descárgalo de https://www.python.org/
    pause
    exit /b 1
)

echo ✅ Python detectado

REM Verificar si existe el archivo .env
if not exist ".env" (
    echo.
    echo ⚠️  Archivo .env no encontrado
    echo Copia .env.example a .env y complétalo
    pause
    exit /b 1
)

echo ✅ Archivo .env encontrado

REM Instalar dependencias
echo.
echo ⏳ Instalando dependencias...
pip install -r requirements.txt >nul 2>&1

if errorlevel 1 (
    echo ❌ Error instalando dependencias
    pip install -r requirements.txt
    pause
    exit /b 1
)

echo ✅ Dependencias instaladas

REM Ejecutar backend
echo.
echo 🚀 Iniciando backend...
cd backend
python app.py

pause
