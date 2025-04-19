import gspread
from oauth2client.service_account import ServiceAccountCredentials

SHEET_URL = "https://docs.google.com/spreadsheets/d/1GgQ22mP1hyqoIfmIjWB_d6_-AAYq-4uHLzTWELHV0ho/edit?gid=0#gid=0"
CREDS_FILE = "advance-block-401512-159f509ef4c3.json" 

def get_pending_tasks():
    creds = ServiceAccountCredentials.from_json_keyfile_name(
        CREDS_FILE,
        ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    )
    sheet = gspread.authorize(creds).open_by_url(SHEET_URL).sheet1
    rows = sheet.get_all_records()
    tasks = []
    for row in rows:
        task = {
            "description": row.get("Asset description"),
            "link": row.get("Link"),
            "format": row.get("Output format"),
            "model": row.get("Tools")
        }
        tasks.append(task)
    return tasks


