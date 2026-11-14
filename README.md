# 🎬 YouTube Downloader Web (.mp4 / .mp3)

<p align="center">
  <a href="#-english"><b>English</b></a> • <a href="#-español"><b>Español</b></a>
</p>

<p align="center">
  <a href="https://opensource.org/licenses/MIT"><img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License: MIT"></a>
  <a href="https://www.python.org/downloads/"><img src="https://img.shields.io/badge/python-3.10+-blue.svg" alt="Python 3.10+"></a>
  <a href="https://flask.palletsprojects.com/"><img src="https://img.shields.io/badge/Flask-3.x-lightgrey.svg" alt="Flask"></a>
  <a href="https://github.com/yt-dlp/yt-dlp"><img src="https://img.shields.io/badge/powered%20by-yt--dlp-red.svg" alt="yt-dlp"></a>
  <a href="https://systemd.io/"><img src="https://img.shields.io/badge/service-systemd--ready-green.svg" alt="Linux Systemd"></a>
</p>

---

## 🇬🇧 English

A modern, fast, and local web application to download YouTube videos and audio with custom quality selection, real-time progress, and zero ads. Includes bilingual UI support (English by default, with an instant switch to Spanish).

### ✨ Features

- 🎨 **Modern & Responsive Web UI**: Clean dark theme built with Tailwind CSS, Lucide icons, and bilingual support (EN/ES switcher).
- 📋 **One-Click Paste**: Quick button to paste YouTube URLs directly from the clipboard.
- 🔍 **Instant Metadata Preview**: Displays video title, author, duration, and thumbnail before downloading.
- 🎬 **Video MP4**:
  - Dynamic resolution picker: **Best available**, **4K (2160p)**, **2K (1440p)**, **1080p (Full HD)**, **720p (HD)**, **480p**, and **360p**.
  - Prioritizes universal **H.264 (AVC1)** video and **AAC** audio for maximum compatibility with all media players and video editors.
- 🎵 **Audio MP3**:
  - High-fidelity audio extraction with selectable bitrate: **320 kbps (Peak fidelity)**, **256 kbps**, **192 kbps (Standard CD)**, and **128 kbps (Lightweight)**.
  - Automatic ID3 metadata and tag embedding.
- ⚡ **Real-Time Progress Tracking**: Live interactive progress bar with percentage, download speed (MB/s), and estimated time remaining (ETA).
- 📂 **Dual Save Options**:
  - Download directly to your browser.
  - Automatic storage in the local `./downloads` folder with a one-click button to open the folder in your operating system.
- 🐧 **Background Service Ready**: Native integration as a Linux `systemd --user` service for seamless background operation.

### 🚀 Prerequisites

- **Python 3.10** or higher.
- **FFmpeg** installed on your system (`sudo apt install ffmpeg`).

### 🛠️ Quick Installation & Usage

1. **Clone the repository:**
   ```bash
   git clone https://github.com/FloxTBoTyy/youtube-downloader-web.git
   cd youtube-downloader-web
   ```

2. **Start the application:**
   ```bash
   chmod +x start.sh
   ./start.sh
   ```
   *The script automatically sets up a `.venv` virtual environment, installs/updates dependencies, and launches your default browser.*

3. **Open in your browser:**
   - **http://descargador-yt.localhost:5050**
   - or http://127.0.0.1:5050

### ⚙️ Running as a System Background Service (Linux / Ubuntu)

To keep the downloader running continuously in the background on boot without needing an open terminal:

1. **Create the user systemd folder:**
   ```bash
   mkdir -p ~/.config/systemd/user
   ```

2. **Create `~/.config/systemd/user/youtube-downloader.service`:**
   ```ini
   [Unit]
   Description=YouTube Downloader Web Service
   After=network.target

   [Service]
   Type=simple
   WorkingDirectory=/path/to/youtube-downloader-web
   Environment=PORT=5050
   Environment=PYTHONUNBUFFERED=1
   ExecStart=/path/to/youtube-downloader-web/.venv/bin/python app.py
   Restart=always
   RestartSec=3

   [Install]
   WantedBy=default.target
   ```

3. **Enable and start the service:**
   ```bash
   systemctl --user daemon-reload
   systemctl --user enable --now youtube-downloader.service
   ```

4. **Useful management commands:**
   ```bash
   # Check service status
   systemctl --user status youtube-downloader.service

   # Restart service
   systemctl --user restart youtube-downloader.service
   ```

### ⚖️ Legal Disclaimer

> [!IMPORTANT]
> This project was developed strictly for **educational and personal backup purposes**. 
> 
> It is designed to allow users to archive their own audiovisual content, public domain material, or content distributed under permissive open licenses (such as *Creative Commons*). The author does not endorse, promote, or take responsibility for any unauthorized downloading, copyright infringement, or violation of YouTube Terms of Service by third parties.
> 
> Always respect intellectual property rights and the applicable copyright laws in your jurisdiction.

---

## 🇪🇸 Español

Aplicación web local, rápida y moderna para descargar videos y audios de YouTube fácilmente seleccionando el formato y la calidad exacta deseada, con barra de progreso en vivo y sin anuncios. Incluye interfaz bilingüe (inglés por defecto y conmutador instantáneo a español).

### ✨ Características Principales

- 🎨 **Interfaz Web Moderna & Responsiva**: Diseñada con Tailwind CSS en tema oscuro, adaptable a cualquier pantalla con selector de idioma (EN/ES).
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

### 🚀 Requisitos Previos

- **Python 3.10** o superior.
- **FFmpeg** instalado en el sistema (`sudo apt install ffmpeg`).

### 🛠️ Instalación y Uso Rápido

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

3. **Abrir en el navegador:**
   - **http://descargador-yt.localhost:5050**
   - o http://127.0.0.1:5050

### ⚙️ Ejecutar como Servicio del Sistema (Linux / Ubuntu)

1. **Crear archivo de servicio `~/.config/systemd/user/youtube-downloader.service`:**
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

2. **Habilitar e iniciar:**
   ```bash
   systemctl --user daemon-reload
   systemctl --user enable --now youtube-downloader.service
   ```

### ⚖️ Descargo de Responsabilidad Legal (Disclaimer)

> [!IMPORTANT]
> Este proyecto ha sido desarrollado con fines exclusivamente **educativos y de respaldo/copia de seguridad personal**. 
> 
> Está diseñado para que los usuarios puedan archivar su propio contenido audiovisual, material de dominio público o contenido distribuido bajo licencias abiertas permisivas (como *Creative Commons*). El autor de este software no promueve, respalda ni se hace responsable del uso indebido que terceros puedan darle en violación de los derechos de propiedad intelectual o de los Términos de Servicio de las plataformas proveedoras. 
> 
> Respeta siempre el trabajo de los creadores de contenido y las leyes de propiedad intelectual aplicables en tu jurisdicción.

---

## 📄 License / Licencia

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.
