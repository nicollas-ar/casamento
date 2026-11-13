import io
import os
import uuid
import logging
from datetime import datetime, timezone

from flask import Flask, render_template, request, jsonify
from werkzeug.exceptions import RequestEntityTooLarge
from werkzeug.middleware.proxy_fix import ProxyFix
from PIL import Image, ImageOps, UnidentifiedImageError
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request as GoogleRequest
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY") or os.urandom(32)
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1)
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024
logging.basicConfig(level=logging.INFO)
SCOPES = ["https://www.googleapis.com/auth/drive.file"]

def drive_service():
    keys = ("GOOGLE_CLIENT_ID", "GOOGLE_CLIENT_SECRET", "GOOGLE_REFRESH_TOKEN", "GOOGLE_DRIVE_FOLDER_ID")
    missing = [key for key in keys if not os.getenv(key)]
    if missing:
        raise RuntimeError("Configuração incompleta: " + ", ".join(missing))
    credentials = Credentials(None,
        refresh_token=os.environ["GOOGLE_REFRESH_TOKEN"],
        token_uri="https://oauth2.googleapis.com/token",
        client_id=os.environ["GOOGLE_CLIENT_ID"],
        client_secret=os.environ["GOOGLE_CLIENT_SECRET"],
        scopes=SCOPES)
    credentials.refresh(GoogleRequest())
    return build("drive", "v3", credentials=credentials, cache_discovery=False)

def prepare_photo(upload):
    extension = (upload.filename or "").lower().rsplit(".", 1)[-1]
    if extension not in ("jpg", "jpeg", "png", "webp"):
        raise ValueError("Escolha imagens JPG, PNG ou WebP.")
    try:
        image = Image.open(upload.stream)
        image.verify()
        upload.stream.seek(0)
        image = ImageOps.exif_transpose(Image.open(upload.stream))
        if image.width * image.height > 60_000_000:
            raise ValueError("Imagem grande demais.")
        image.thumbnail((4000, 4000), Image.Resampling.LANCZOS)
        output = io.BytesIO()
        image.convert("RGB").save(output, "JPEG", quality=90, optimize=True)
        output.seek(0)
        return output
    except (UnidentifiedImageError, OSError, ValueError) as exc:
        raise ValueError("Imagem inválida. Envie JPG, PNG ou WebP.") from exc

@app.get("/")
def home():
    return render_template("index.html",
        couple=os.getenv("COUPLE_NAMES", "Nosso casamento"),
        date=os.getenv("WEDDING_DATE", "Um dia para recordar"),
        heading=os.getenv("WEDDING_HEADING", "Cada momento merece ser lembrado."))

@app.post("/enviar")
def enviar():
    photos = request.files.getlist("fotos")
    if not photos or len(photos) > 2:
        return jsonify(error="Selecione de 1 a 2 fotos."), 400
    sent = 0
    try:
        service = drive_service()
        for photo in photos:
            data = prepare_photo(photo)
            timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
            name = f"{timestamp}_{uuid.uuid4().hex[:10]}.jpg"
            metadata = {"name": name,
                        "parents": [os.environ["GOOGLE_DRIVE_FOLDER_ID"]],
                        "description": "Foto enviada pelo álbum do casamento"}
            media = MediaIoBaseUpload(data, mimetype="image/jpeg", resumable=False)
            service.files().create(body=metadata, media_body=media, fields="id", supportsAllDrives=True).execute()
            sent += 1
        return jsonify(ok=True, enviados=sent)
    except ValueError as exc:
        return jsonify(error=str(exc), enviados=sent), 400
    except Exception:
        app.logger.exception("Falha no envio ao Google Drive")
        return jsonify(error="Não foi possível concluir o envio. Tente novamente.", enviados=sent), 502

@app.get("/saude")
def saude():
    return jsonify(status="ok")

@app.errorhandler(RequestEntityTooLarge)
def too_large(_):
    return jsonify(error="Limite de 16 MB por envio. Escolha menos fotos."), 413

if __name__ == "__main__":
    app.run(debug=os.getenv("FLASK_DEBUG") == "1", port=int(os.getenv("PORT", 5000)))
