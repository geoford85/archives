# ~/Desktop/archives/reading_list_generator.py

import os
import json
from datetime import datetime
from collections import defaultdict

CATALOG_FILE = "library_catalog.json"
STATUS_FILE = "book_status.json"
PROGRESS_FILE = "reading_progress.json"

def load_json(path):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def get_reading_list():
    catalog = load_json(CATALOG_FILE)
    status = load_json(STATUS_FILE)
    progress = load_json(PROGRESS_FILE)

    suggestions = []

    # Group by series
    series_tracker = defaultdict(list)
    for book in catalog:
        series = book.get("series")
        if not series:
            continue
        series_tracker[series].append(book)

    # Look for series in progress or untouched
    for series, books in series_tracker.items():
        in_progress = any(
            status.get(book.get("id"), {}).get("status") == "in progress" for book in books
        )
        to_be_read = [
            book for book in books
            if status.get(book.get("id"), {}).get("status") == "to be read"
        ]

        if in_progress or to_be_read:
            suggestions.append(f"📚 {series}: {len(to_be_read)} book(s) left")

    # Add individual books not in a series
    for book in catalog:
        if not book.get("series") and status.get(book.get("id"), {}).get("status") == "to be read":
            suggestions.append(f"📘 {book.get('title')} (standalone)")

    if suggestions:
        print("\n📜 Suggested Reading List:\n")
        for item in suggestions:
            print(f" - {item}")
    else:
        print("🎉 You have no unfinished books or series. Time to go book shopping!")

if __name__ == "__main__":
    get_reading_list()

