
import json
import os

PROGRESS_FILE = "reading_progress.json"

def load_progress():
    if os.path.exists(PROGRESS_FILE):
        with open(PROGRESS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_progress(data):
    with open(PROGRESS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def get_progress(book_title):
    progress = load_progress()
    return progress.get(book_title, "No progress found for that book.")

def update_progress(book_title, location):
    progress = load_progress()
    progress[book_title] = location
    save_progress(progress)
    return f"✅ Progress for '{book_title}' updated to: {location}"
