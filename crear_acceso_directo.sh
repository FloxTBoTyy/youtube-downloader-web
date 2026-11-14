#!/bin/bash

DIR="$(cd "$(dirname "$0")" && pwd)"
DESKTOP_DIR="$HOME/Escritorio"
[ ! -d "$DESKTOP_DIR" ] && DESKTOP_DIR="$HOME/Desktop"

DESKTOP_FILE="$DESKTOP_DIR/youtube-downloader.desktop"

cat <<EOF > "$DESKTOP_FILE"
[Desktop Entry]
Version=1.0
Type=Application
Name=YouTube Downloader Web
Comment=Descarga videos y audios de YouTube en MP4 y MP3
Exec=bash -c "cd '$DIR' && ./start.sh"
Icon=video-x-generic
Terminal=true
Categories=AudioVideo;Network;
EOF

chmod +x "$DESKTOP_FILE"
# Configurar permiso de ejecución para GNOME si gio está disponible
if command -v gio &> /dev/null; then
    gio set "$DESKTOP_FILE" metadata::trusted true 2>/dev/null || true
fi

echo "✅ Acceso directo creado en: $DESKTOP_FILE"
