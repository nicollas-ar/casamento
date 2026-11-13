"""Execute uma vez no seu computador. Nunca publique credenciais ou tokens."""
import os
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

if not os.path.exists("credentials.json"):
    raise SystemExit("Baixe o arquivo OAuth do tipo Aplicativo para computador e salve como credentials.json.")

flow = InstalledAppFlow.from_client_secrets_file(
    "credentials.json",
    scopes=["https://www.googleapis.com/auth/drive.file"],
)
credentials = flow.run_local_server(port=0, access_type="offline", prompt="consent")
if not credentials.refresh_token:
    raise SystemExit("O Google não retornou refresh token. Revogue a autorização e execute novamente.")

service = build("drive", "v3", credentials=credentials, cache_discovery=False)
folder = service.files().create(
    body={"name": "Fotos do Casamento", "mimeType": "application/vnd.google-apps.folder"},
    fields="id,webViewLink",
).execute()

print("\nPasta criada no Drive: " + folder.get("webViewLink", "https://drive.google.com/drive/folders/" + folder["id"]))
print("\nCopie os valores abaixo SOMENTE para Environment no Render (não envie no chat):")
print("GOOGLE_CLIENT_ID:", credentials.client_id)
print("GOOGLE_CLIENT_SECRET:", credentials.client_secret)
print("GOOGLE_REFRESH_TOKEN:", credentials.refresh_token)
print("GOOGLE_DRIVE_FOLDER_ID:", folder["id"])
