#!/bin/bash

# Navegar al directorio del script
cd "$(dirname "$0")" || exit 1

PORT=5050
URL="http://descargador-yt.localhost:$PORT"

echo "=========================================================="
echo "  🎬 Iniciando YouTube Downloader Web (.mp4 / .mp3)       "
echo "=========================================================="

# 1. Crear entorno virtual si no existe
if [ ! -d ".venv" ]; then
    echo "⚙️ Creando entorno virtual .venv..."
    python3 -m venv .venv
fi

# 2. Instalar / actualizar dependencias
echo "📦 Verificando dependencias..."
.venv/bin/pip install --upgrade -q pip
.venv/bin/pip install -q -r requirements.txt
.venv/bin/pip install --upgrade -q yt-dlp

# 3. Abrir navegador en segundo plano después de 1 segundo
(sleep 1 && (xdg-open "$URL" 2>/dev/null || sensible-browser "$URL" 2>/dev/null || x-www-browser "$URL" 2>/dev/null || echo "Abre en tu navegador: $URL")) &

echo ""
echo "🚀 Servidor listo en: $URL"
echo "📁 Carpeta de descargas: $(pwd)/downloads"
echo "Para detener el servidor presiona Ctrl+C"
echo "=========================================================="
echo ""

# 4. Iniciar aplicación Flask
export PORT=$PORT
exec .venv/bin/python app.py
