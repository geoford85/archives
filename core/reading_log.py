# ~/Desktop/archives/reading_log.py

import json
import os
from datetime import datetime

LOG_FILE = "reading_log.json"

def load_log():
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_log(log_entries):
    with open(LOG_FILE, "w", encoding="utf-8") as f:
        json.dump(log_entries, f, indent=2, ensure_ascii=False)

def log_finished_book(book_id, title, author=None, series=None):
    log_entries = load_log()

    log_entries.append({
        "book_id": book_id,
        "title": title,
        "author": author,
        "series": series,
        "date_finished": datetime.now().strftime("%Y-%m-%d")
    })

    save_log(log_entries)
    print(f"📚 Logged '{title}' as finished on {datetime.now().strftime('%Y-%m-%d')}.")

def get_books_by_month(month_str):
    # Format: "2025-04"
    log_entries = load_log()
    matches = [
        entry for entry in log_entries
        if entry["date_finished"].startswith(month_str)
    ]

    if matches:
        print(f"\n📅 Books read in {month_str}:")
        for entry in matches:
            print(f"✅ {entry['title']} by {entry.get('author', 'Unknown')}")
    else:
        print(f"No books logged for {month_str}.")

# Example usage
if __name__ == "__main__":
    # Sample log entry
    log_finished_book(
        book_id="abc123xyz",
        title="Cradle: Uncrowned",
        author="Will Wight",
        series="Cradle"
    )

    # View a specific month (edit date as needed)
    get_books_by_month("2025-04")

