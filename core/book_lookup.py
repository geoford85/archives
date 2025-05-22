# ~/Desktop/archives/book_lookup.py

import os
import json
import difflib

CATALOG_FILE = "library_catalog.json"

def load_catalog():
    if not os.path.exists(CATALOG_FILE):
        return []
    with open(CATALOG_FILE, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def find_book_id_by_title(query):
    catalog = load_catalog()
    titles = {book["title"]: book["id"] for book in catalog if "title" in book and "id" in book}

    if query in titles:
        return titles[query]

    # Fuzzy match
    close_matches = difflib.get_close_matches(query, titles.keys(), n=1, cutoff=0.6)
    if close_matches:
        best_match = close_matches[0]
        print(f"🔍 Did you mean '{best_match}'?")
        return titles[best_match]

    print("❌ No match found.")
    return None

def find_book_by_title(query):
    catalog = load_catalog()
    for book in catalog:
        if book.get("title", "").lower() == query.lower():
            return book
    # Try fuzzy
    close_matches = difflib.get_close_matches(query, [b.get("title", "") for b in catalog], n=1, cutoff=0.6)
    if close_matches:
        for book in catalog:
            if book.get("title") == close_matches[0]:
                print(f"🔍 Found closest match: {book.get('title')}")
                return book
    print("❌ No matching book found.")
    return None

# Test
if __name__ == "__main__":
    result = find_book_by_title("Uncrowned")
    if result:
        print(f"✅ Book ID: {result['id']}")
