# ~/Desktop/archives/reading_progress.py

import os
import json
from datetime import datetime

PROGRESS_FILE = "reading_progress.json"

def load_progress():
    if os.path.exists(PROGRESS_FILE):
        with open(PROGRESS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_progress(progress):
    with open(PROGRESS_FILE, "w", encoding="utf-8") as f:
        json.dump(progress, f, indent=2, ensure_ascii=False)

def update_progress(book_id, title, series=None, location="Unknown"):
    progress = load_progress()

    progress[book_id] = {
        "title": title,
        "series": series,
        "last_location": location,
        "last_updated": datetime.now().strftime("%Y-%m-%d")
    }

    save_progress(progress)
    print(f"📍 Updated progress for '{title}' → {location}")

def get_progress(book_id):
    progress = load_progress()
    return progress.get(book_id, None)

# Example usage
if __name__ == "__main__":
    # Sample: Update progress
    update_progress(
        book_id="abc123xyz",
        title="Cradle: Uncrowned",
        series="Cradle",
        location="Chapter 14"
    )

    # Sample: Retrieve progress
    info = get_progress("abc123xyz")
    if info:
        print(f"📖 Last seen in '{info['title']}' at {info['last_location']} on {info['last_updated']}")
    else:
        print("No progress recorded for this book.")

