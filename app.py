import os
import glob
import subprocess
import threading
import uuid
import time
from flask import Flask, render_template, request, jsonify, send_file
import yt_dlp

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DOWNLOADS_DIR = os.path.join(BASE_DIR, "downloads")
os.makedirs(DOWNLOADS_DIR, exist_ok=True)

# In-memory storage for active download tasks
tasks = {}

def format_duration(seconds):
    if not seconds:
        return "Desconocida"
    m, s = divmod(int(seconds), 60)
    h, m = divmod(m, 60)
    if h > 0:
        return f"{h}:{m:02d}:{s:02d}"
    return f"{m}:{s:02d}"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/info", methods=["POST"])
def get_video_info():
    data = request.get_json() or {}
    url = data.get("url", "").strip()
    if not url:
        return jsonify({"error": "Por favor ingresa un enlace válido de YouTube."}), 400

    ydl_opts = {
        "quiet": True,
        "no_warnings": True,
        "skip_download": True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)

        # Extract available video resolutions
        resolutions = set()
        for f in info.get("formats", []):
            h = f.get("height")
            vcodec = f.get("vcodec", "none")
            if h and vcodec != "none" and isinstance(h, int):
                resolutions.add(h)

        sorted_res = sorted(list(resolutions), reverse=True)
        # Filter common standard resolutions
        standard_res = [2160, 1440, 1080, 720, 480, 360, 240]
        available_res = [r for r in standard_res if any(abs(r - sr) <= 20 for sr in sorted_res)]
        if not available_res and sorted_res:
            available_res = sorted_res[:5]

        return jsonify({
            "id": info.get("id"),
            "title": info.get("title", "Video sin título"),
            "uploader": info.get("uploader") or info.get("channel", "Canal desconocido"),
            "duration": format_duration(info.get("duration")),
            "thumbnail": info.get("thumbnail", ""),
            "resolutions": available_res or [1080, 720, 480, 360]
        })
    except Exception as e:
        return jsonify({"error": f"No se pudo obtener información del video: {str(e)}"}), 400

def _execute_download(task_id, url, format_type, quality):
    tasks[task_id]["status"] = "downloading"
    tasks[task_id]["progress"] = 0
    tasks[task_id]["speed"] = "--"
    tasks[task_id]["eta"] = "--"

    def progress_hook(d):
        if d.get("status") == "downloading":
            tasks[task_id]["status"] = "downloading"
            total = d.get("total_bytes") or d.get("total_bytes_estimate") or 0
            downloaded = d.get("downloaded_bytes", 0)
            if total > 0:
                tasks[task_id]["progress"] = round((downloaded / total) * 100, 1)
            else:
                tasks[task_id]["progress"] = 50.0  # approximate

            speed = d.get("speed")
            if speed:
                if speed > 1024 * 1024:
                    tasks[task_id]["speed"] = f"{speed / (1024 * 1024):.1f} MB/s"
                else:
                    tasks[task_id]["speed"] = f"{speed / 1024:.0f} KB/s"
            else:
                tasks[task_id]["speed"] = d.get("_speed_str", "--")

            tasks[task_id]["eta"] = d.get("_eta_str", "--")

        elif d.get("status") == "finished":
            tasks[task_id]["status"] = "processing"
            tasks[task_id]["progress"] = 99.0

    out_template = os.path.join(DOWNLOADS_DIR, f"%(title)s [{task_id}].%(ext)s")

    ydl_opts = {
        "outtmpl": out_template,
        "progress_hooks": [progress_hook],
        "quiet": True,
        "no_warnings": True,
    }

    if format_type == "mp3":
        bitrate = quality if quality in ["320", "256", "192", "128"] else "320"
        ydl_opts.update({
            "format": "bestaudio/best",
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": bitrate,
                },
                {
                    "key": "FFmpegMetadata",
                    "add_metadata": True,
                }
            ],
        })
    else:
        # MP4 Video: prioritize universally compatible H.264/AVC1 + AAC
        if quality == "best":
            format_str = "bestvideo[vcodec^=avc1]+bestaudio[ext=m4a]/bestvideo[ext=mp4]+bestaudio[ext=m4a]/bestvideo+bestaudio/best"
        else:
            try:
                h = int(quality)
                format_str = f"bestvideo[height<={h}][vcodec^=avc1]+bestaudio[ext=m4a]/bestvideo[height<={h}][ext=mp4]+bestaudio[ext=m4a]/bestvideo[height<={h}]+bestaudio/best[height<={h}]/best"
            except ValueError:
                format_str = "bestvideo[vcodec^=avc1]+bestaudio[ext=m4a]/bestvideo[ext=mp4]+bestaudio[ext=m4a]/bestvideo+bestaudio/best"

        ydl_opts.update({
            "format": format_str,
            "merge_output_format": "mp4",
            "postprocessors": [
                {
                    "key": "FFmpegVideoConvertor",
                    "preferedformat": "mp4",
                }
            ],
        })

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        # Find the resulting downloaded file using task_id
        matching_files = glob.glob(os.path.join(DOWNLOADS_DIR, f"*{task_id}*.*"))
        if matching_files:
            final_file = matching_files[0]
            tasks[task_id]["status"] = "finished"
            tasks[task_id]["progress"] = 100.0
            tasks[task_id]["filepath"] = final_file
            tasks[task_id]["filename"] = os.path.basename(final_file)
            tasks[task_id]["filesize"] = f"{os.path.getsize(final_file) / (1024 * 1024):.2f} MB"
        else:
            tasks[task_id]["status"] = "finished"
            tasks[task_id]["progress"] = 100.0
    except Exception as e:
        tasks[task_id]["status"] = "error"
        tasks[task_id]["error"] = str(e)

@app.route("/api/download", methods=["POST"])
def start_download():
    data = request.get_json() or {}
    url = data.get("url", "").strip()
    format_type = data.get("format", "mp4").strip().lower()
    quality = str(data.get("quality", "best")).strip()

    if not url:
        return jsonify({"error": "URL inválida."}), 400

    task_id = uuid.uuid4().hex[:8]
    tasks[task_id] = {
        "status": "queued",
        "progress": 0,
        "format": format_type,
        "quality": quality,
        "filename": None,
        "filepath": None,
        "error": None,
        "created_at": time.time(),
    }

    thread = threading.Thread(
        target=_execute_download,
        args=(task_id, url, format_type, quality),
        daemon=True
    )
    thread.start()

    return jsonify({"task_id": task_id})

@app.route("/api/progress/<task_id>", methods=["GET"])
def check_progress(task_id):
    task = tasks.get(task_id)
    if not task:
        return jsonify({"error": "Tarea no encontrada."}), 404
    return jsonify(task)

@app.route("/api/download-file/<task_id>", methods=["GET"])
def download_file(task_id):
    task = tasks.get(task_id)
    if not task or not task.get("filepath") or not os.path.exists(task["filepath"]):
        return jsonify({"error": "Archivo no disponible."}), 404

    return send_file(
        task["filepath"],
        as_attachment=True,
        download_name=task.get("filename")
    )

@app.route("/api/open-folder", methods=["POST"])
def open_folder():
    try:
        subprocess.Popen(["xdg-open", DOWNLOADS_DIR])
        return jsonify({"success": True, "message": "Carpeta abierta en el explorador de archivos."})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5050))
    print(f"\n=======================================================")
    print(f"  🚀 YouTube Downloader Web iniciado en:")
    print(f"     http://127.0.0.1:{port}")
    print(f"     Carpeta de descargas: {DOWNLOADS_DIR}")
    print(f"=======================================================\n")
    app.run(host="0.0.0.0", port=port, debug=False)
