# ~/Desktop/archives/scanner.py

import os
import json
from epub_parser import extract_epub_metadata
from config import LIBRARY_PATH, CATALOG_PATH

def load_catalog():
    if os.path.exists(CATALOG_PATH):
        with open(CATALOG_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_catalog(catalog):
    with open(CATALOG_PATH, "w", encoding="utf-8") as f:
        json.dump(catalog, f, indent=2, ensure_ascii=False)

def scan_for_epubs():
    catalog = load_catalog()
    known_paths = set(book["file_path"] for book in catalog)

    new_books = []

    for root, _, files in os.walk(LIBRARY_PATH):
        for file in files:
            if file.lower().endswith(".epub"):
                full_path = os.path.abspath(os.path.join(root, file))
                if full_path not in known_paths:
                    try:
                        metadata = extract_epub_metadata(full_path)
                        new_books.append(metadata)
                        print(f"✓ Added: {metadata['title'] or file}")
                    except Exception as e:
                        print(f"⚠️ Failed to process {file}: {e}")

    if new_books:
        catalog.extend(new_books)
        save_catalog(catalog)
        print(f"📘 {len(new_books)} new EPUB(s) added.")
    else:
        print("✨ No new EPUBs found.")

if __name__ == "__main__":
    scan_for_epubs()

