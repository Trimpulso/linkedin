#!/bin/bash

echo ""
echo "╔════════════════════════════════════════════════════════╗"
echo "║                                                        ║"
echo "║   🤖 LINKEDIN CHATBOT - Iniciando Sistema...          ║"
echo "║                                                        ║"
echo "╚════════════════════════════════════════════════════════╝"
echo ""

# Verificar Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 no está instalado"
    echo "Instálalo con: sudo apt-get install python3"
    exit 1
fi

echo "✅ Python detectado"

# Verificar .env
if [ ! -f ".env" ]; then
    echo ""
    echo "⚠️  Archivo .env no encontrado"
    echo "Copia .env.example a .env y complétalo"
    exit 1
fi

echo "✅ Archivo .env encontrado"

# Instalar dependencias
echo ""
echo "⏳ Instalando dependencias..."
pip3 install -r requirements.txt >/dev/null 2>&1

if [ $? -ne 0 ]; then
    echo "❌ Error instalando dependencias"
    pip3 install -r requirements.txt
    exit 1
fi

echo "✅ Dependencias instaladas"

# Ejecutar backend
echo ""
echo "🚀 Iniciando backend..."
cd backend
python3 app.py
