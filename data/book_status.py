# ~/Desktop/archives/book_status.py

import os
import json
from datetime import datetime

STATUS_FILE = "book_status.json"
VALID_STATUSES = {"read", "in progress", "to be read", "did not finish"}

def load_status():
    if os.path.exists(STATUS_FILE):
        with open(STATUS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_status(status_data):
    with open(STATUS_FILE, "w", encoding="utf-8") as f:
        json.dump(status_data, f, indent=2, ensure_ascii=False)

def update_status(book_id, title, status):
    if status not in VALID_STATUSES:
        print(f"❌ Invalid status: {status}")
        print(f"Valid options are: {', '.join(VALID_STATUSES)}")
        return

    data = load_status()

    data[book_id] = {
        "title": title,
        "status": status,
        "last_updated": datetime.now().strftime("%Y-%m-%d")
    }

    save_status(data)
    print(f"🧿 Updated status for '{title}' → {status}")

def get_status(book_id):
    data = load_status()
    return data.get(book_id, None)

# Example usage
if __name__ == "__main__":
    # Sample: update status
    update_status(
        book_id="abc123xyz",
        title="Cradle: Uncrowned",
        status="in progress"
    )

    # Sample: retrieve status
    info = get_status("abc123xyz")
    if info:
        print(f"📘 '{info['title']}' is marked as '{info['status']}' (updated {info['last_updated']})")
    else:
        print("No status info recorded for this book.")

