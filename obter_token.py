"""Execute uma vez no computador. Nunca publique credenciais."""
import os
from google_auth_oauthlib.flow import InstalledAppFlow

if not os.path.exists("credentials.json"):
    raise SystemExit("Baixe o JSON do cliente OAuth desktop e salve como credentials.json.")

flow = InstalledAppFlow.from_client_secrets_file(
    "credentials.json",
    scopes=["https://www.googleapis.com/auth/drive.file"],
)
credentials = flow.run_local_server(port=0, access_type="offline", prompt="consent")
print("Copie estes valores para Environment no Render; nunca publique ou compartilhe:")
print("GOOGLE_CLIENT_ID:", credentials.client_id)
print("GOOGLE_CLIENT_SECRET:", credentials.client_secret)
print("GOOGLE_REFRESH_TOKEN:", credentials.refresh_token)
