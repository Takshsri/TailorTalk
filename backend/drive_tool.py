from google.oauth2 import service_account
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/drive.readonly']

SERVICE_ACCOUNT_FILE = 'service-account.json'

FOLDER_ID = "1qkx58doSeYrcLjHPDysJyVJ36PsSqqlt"

creds = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE,
    scopes=SCOPES
)

service = build('drive', 'v3', credentials=creds)


def search_drive(query):
    drive_query = f"'{FOLDER_ID}' in parents and {query}"

    results = service.files().list(
        q=drive_query,
        pageSize=10,
        fields="files(id, name, mimeType, modifiedTime, webViewLink)"
    ).execute()

    files = results.get('files', [])

    if not files:
        return "No matching files found."

    output = []

    for file in files:
        output.append(
    f"""
📄 **{file['name']}**

- Type: {file['mimeType']}
- Modified: {file['modifiedTime']}
- [Open File]({file['webViewLink']})

---
"""
)

    return "\n".join(output)