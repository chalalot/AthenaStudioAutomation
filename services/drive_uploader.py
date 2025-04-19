from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

def upload_to_drive(file_path: str, filename: str, folder_id: str) -> tuple[bool, str]:
    try:
        # Load credentials
        creds = service_account.Credentials.from_service_account_file(
            "advance-block-401512-159f509ef4c3.json",
            scopes=["https://www.googleapis.com/auth/drive"]
        )

        service = build("drive", "v3", credentials=creds)

        # Set metadata
        file_metadata = {
            "name": filename,
            "parents": [folder_id]
        }

        media = MediaFileUpload(file_path, mimetype="image/png")

        uploaded_file = service.files().create(
            body=file_metadata,
            media_body=media,
            fields="id"
        ).execute()

        file_id = uploaded_file.get("id")
        file_link = f"https://drive.google.com/file/d/{file_id}/view"

        # Share the file publicly
        service.permissions().create(
            fileId=file_id,
            body={
                "role": "reader",
                "type": "anyone"
            }
        ).execute()

        print(f"✅ File uploaded: {file_link}")
        return True, file_link

    except Exception as e:
        print(f"❌ Upload failed: {e}")
        return False, str(e)
