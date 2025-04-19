from services.sheet_reader import get_pending_tasks
from services.image_downloader import fetch_image
from services.image_generator import generate_image
from services.drive_uploader import upload_to_drive
from services.logger import log_task, init_db
from services.notifier import send_email_notification, send_slack_message
from config import DRIVE_FOLDER_ID

def main():
    init_db()
    tasks = get_pending_tasks()
    print("🔄 Starting automation...")
    print(f"Loaded {len(tasks)} tasks")
    print(DRIVE_FOLDER_ID)
    # Fetch tasks from Google Sheets
    for task in tasks:
        try:
            print(f"\n🟢 Processing: {task['description'][:50]}")
            # Download reference image
            reference_path = fetch_image(task["link"])
            # Generate image
            output_path = generate_image(prompt=task["description"] ,image_path=reference_path, output_format=task["format"])
            print(f"Generated image saved at: {output_path}")
            # Upload to Google Drive
            status, drive_url = upload_to_drive(output_path, "generated.png", DRIVE_FOLDER_ID)
            print(f"Uploaded to: {drive_url}")
            # Log and notify
            log_task(task_id=task["description"], status=status, message=drive_url)
            send_email_notification(success=status, body=f"✅ Task complete: {drive_url} successfully")
            send_slack_message(success=status, message=f"✅ Task complete: {drive_url}")

        except Exception as e:
            log_task(task_id=task["description"], status=status, message=str(e))
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
