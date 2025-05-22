# ~/Desktop/archives/reindexer.py

import os
import json

CATALOG_FILE = "library_catalog.json"
SCAN_DIR = "Bookshelf"  # Adjust this if needed (e.g., ~/Desktop/archives/Bookshelf)

def load_catalog():
    if os.path.exists(CATALOG_FILE):
        with open(CATALOG_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_catalog(data):
    with open(CATALOG_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def scan_files(base_dir):
    all_files = []
    for root, _, files in os.walk(base_dir):
        for file in files:
            if file.lower().endswith((".epub", ".mobi", ".pdf", ".azw3")):
                relative_path = os.path.relpath(os.path.join(root, file), base_dir)
                all_files.append(relative_path)
    return all_files

def reindex_catalog():
    print("📚 Starting reindex...")

    catalog = load_catalog()
    known_paths = set(book.get("file_path") for book in catalog if book.get("file_path"))
    scanned_files = scan_files(SCAN_DIR)

    new_books = []
    for file_path in scanned_files:
        if file_path not in known_paths:
            new_entry = {
                "title": os.path.splitext(os.path.basename(file_path))[0],
                "author": "Unknown",
                "series": None,
                "series_number": None,
                "format": os.path.splitext(file_path)[1],
                "file_path": file_path,
                "id": None  # To be filled later
            }
            new_books.append(new_entry)

    if new_books:
        print(f"📥 Found {len(new_books)} new book(s). Adding to catalog...")
        catalog.extend(new_books)
        save_catalog(catalog)
    else:
        print("✅ No new books found. Catalog is up to date.")

if __name__ == "__main__":
    reindex_catalog()

