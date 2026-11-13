"""Cria pasta do Drive por meio do app (evita erro 403 com drive.file)."""
import os
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

for key in ("GOOGLE_CLIENT_ID", "GOOGLE_CLIENT_SECRET", "GOOGLE_REFRESH_TOKEN"):
    if not os.getenv(key):
        raise SystemExit("Configure a variável " + key + " no ambiente.")

credentials = Credentials(
    None,
    refresh_token=os.environ["GOOGLE_REFRESH_TOKEN"],
    token_uri="https://oauth2.googleapis.com/token",
    client_id=os.environ["GOOGLE_CLIENT_ID"],
    client_secret=os.environ["GOOGLE_CLIENT_SECRET"],
    scopes=["https://www.googleapis.com/auth/drive.file"],
)
credentials.refresh(Request())
drive = build("drive", "v3", credentials=credentials)
folder = drive.files().create(
    body={"name": "Fotos do Casamento", "mimeType": "application/vnd.google-apps.folder"},
    fields="id,webViewLink",
).execute()
print("GOOGLE_DRIVE_FOLDER_ID:", folder["id"])
print("Pasta:", folder.get("webViewLink", "https://drive.google.com/drive/folders/" + folder["id"]))
