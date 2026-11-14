# 🎬 YouTube Downloader Web (.mp4 / .mp3)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/Flask-3.x-lightgrey.svg)](https://flask.palletsprojects.com/)
[![yt-dlp](https://img.shields.io/badge/powered%20by-yt--dlp-red.svg)](https://github.com/yt-dlp/yt-dlp)
[![Linux Systemd](https://img.shields.io/badge/service-systemd--ready-green.svg)](https://systemd.io/)

Aplicación web local, rápida y moderna para descargar videos y audios de YouTube fácilmente seleccionando el formato y la calidad exacta deseada, con barra de progreso en vivo y sin anuncios.

---

## ✨ Características Principales

- 🎨 **Interfaz Web Moderna & Responsiva**: Diseñada con Tailwind CSS en tema oscuro, adaptable a cualquier pantalla.
- 📋 **Pegado Rápido**: Botón integrado para pegar directamente la URL desde el portapapeles.
- 🔍 **Previsualización Instantánea**: Muestra título, autor, duración y miniatura del video antes de descargar.
- 🎬 **Video MP4**:
  - Selector dinámico de resolución: **Máxima disponible**, **4K (2160p)**, **2K (1440p)**, **1080p (Full HD)**, **720p (HD)**, **480p** y **360p**.
  - Prioriza códec **H.264 (AVC1)** y audio **AAC** para garantizar reproducción universal en cualquier reproductor o editor.
- 🎵 **Audio MP3**:
  - Extracción de audio de alta fidelidad con selector de bitrate: **320 kbps (Máxima fidelidad)**, **256 kbps**, **192 kbps (Estándar CD)** y **128 kbps (Ligero)**.
  - Metadatos ID3 automáticos.
- ⚡ **Progreso en Tiempo Real**: Visualización interactiva con porcentaje (%), velocidad en MB/s y tiempo estimado restante.
- 📂 **Doble Método de Guardado**:
  - Guardar directamente en la carpeta de descargas del navegador.
  - Almacenamiento en carpeta local `./downloads` con botón de acceso directo en el explorador de archivos.
- 🐧 **Servicio en Segundo Plano**: Soporte nativo para ejecutarse como servicio `systemd --user` en Linux.

---

## 🚀 Requisitos Previos

- **Python 3.10** o superior.
- **FFmpeg** instalado en el sistema (`sudo apt install ffmpeg`).

---

## 🛠️ Instalación y Uso Rápido

1. **Clonar el repositorio:**
   ```bash
   git clone https://github.com/FloxTBoTyy/youtube-downloader-web.git
   cd youtube-downloader-web
   ```

2. **Iniciar la aplicación:**
   ```bash
   chmod +x start.sh
   ./start.sh
   ```
   *El script creará automáticamente el entorno virtual `.venv`, instalará/actualizará `yt-dlp` y abrirá la web en tu navegador predeterminado.*

3. **Abrir en el navegador:**
   - **http://descargador-yt.localhost:5050**
   - o http://127.0.0.1:5050

---

## ⚙️ Ejecutar como Servicio del Sistema (Linux / Ubuntu)

Para que el descargador esté siempre activo en segundo plano al encender el equipo sin necesidad de abrir terminales:

1. **Copiar o crear el archivo de servicio:**
   ```bash
   mkdir -p ~/.config/systemd/user
   ```

2. **Crear `~/.config/systemd/user/youtube-downloader.service`:**
   ```ini
   [Unit]
   Description=YouTube Downloader Web Service
   After=network.target

   [Service]
   Type=simple
   WorkingDirectory=/ruta/a/youtube-downloader-web
   Environment=PORT=5050
   Environment=PYTHONUNBUFFERED=1
   ExecStart=/ruta/a/youtube-downloader-web/.venv/bin/python app.py
   Restart=always
   RestartSec=3

   [Install]
   WantedBy=default.target
   ```

3. **Habilitar e iniciar:**
   ```bash
   systemctl --user daemon-reload
   systemctl --user enable --now youtube-downloader.service
   ```

4. **Comandos de gestión:**
   ```bash
   # Comprobar estado
   systemctl --user status youtube-downloader.service

   # Reiniciar servicio
   systemctl --user restart youtube-downloader.service
   ```

---

## ⚖️ Descargo de Responsabilidad Legal (Disclaimer)

> [!IMPORTANT]
> Este proyecto ha sido desarrollado con fines exclusivamente **educativos y de respaldo/copia de seguridad personal**. 
> 
> Está diseñado para que los usuarios puedan archivar su propio contenido audiovisual, material de dominio público o contenido distribuido bajo licencias abiertas permisivas (como *Creative Commons*). El autor de este software no promueve, respalda ni se hace responsable del uso indebido que terceros puedan darle en violación de los derechos de propiedad intelectual o de los Términos de Servicio de las plataformas proveedoras. 
> 
> Respeta siempre el trabajo de los creadores de contenido y las leyes de propiedad intelectual aplicables en tu jurisdicción.

---

## 📄 Licencia

Este proyecto está bajo la Licencia **MIT**. Consulta el archivo [LICENSE](LICENSE) para más detalles.
