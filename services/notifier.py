import yagmail
import os
import requests

def send_email_notification(success: bool, body: str = "", to: str = None):
    subject = "✅ Task Succeeded" if success else "❌ Task Failed"
    to = to or os.getenv("EMAIL_RECIPIENT")

    try:
        yag = yagmail.SMTP(os.getenv("EMAIL_USER"), os.getenv("EMAIL_PASS"))
        yag.send(to=to, subject=subject, contents=body)
        print("📧 Email sent.")
    except Exception as e:
        print(f"❌ Failed to send email: {e}")

def send_slack_message(success: bool, message: str = "", webhook_url: str = None):
    webhook = webhook_url or os.getenv("SLACK_WEBHOOK_URL")
    if not webhook:
        print("❌ No Slack webhook URL provided.")
        return False

    prefix = "✅ *Task Succeeded*" if success else "❌ *Task Failed*"
    payload = {"text": f"{prefix}\n{message}"}

    try:
        response = requests.post(webhook, json=payload)
        if response.status_code == 200:
            print("💬 Slack message sent.")
            return True
        else:
            print(f"❌ Slack error {response.status_code}: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Failed to send Slack message: {e}")
        return False

