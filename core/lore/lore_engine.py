import json
import os
import sys

PROGRESS_FILE = "user_progress.json"
LIBRARY_FILE = "library_catalog.json"  # Replace with Gemini's final file
LORE_FILE = "lore_data.json"

def load_json_file(path):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_json_file(data, path):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def load_library():
    return load_json_file(LIBRARY_FILE)

def load_progress():
    return load_json_file(PROGRESS_FILE)

def save_progress(progress):
    save_json_file(progress, PROGRESS_FILE)

def load_lore():
    return load_json_file(LORE_FILE)

def update_progress(series_name, book_number, chapter):
    progress = load_progress()
    progress[series_name] = {
        "book_number": book_number,
        "chapter": chapter
    }
    save_progress(progress)
    print(f"[Archie] ✅ Progress updated for '{series_name}': Book {book_number}, Chapter {chapter}")

def get_lore(series_name):
    progress = load_progress()
    lore_db = load_lore()

    if series_name not in progress:
        return "[Archie] 📚 No progress found. Use 'update' to set your position first."

    book = str(progress[series_name]["book_number"])
    chapter = progress[series_name]["chapter"]
    lore_entries = []

    if series_name in lore_db and book in lore_db[series_name]:
        for chap_str, summary in lore_db[series_name][book].items():
            if int(chap_str) <= chapter:
                lore_entries.append(f"Chapter {chap_str}: {summary}")

    if not lore_entries:
        return f"[Archie] 🤫 No lore found up to Book {book}, Chapter {chapter}."

    return f"[Archie] Lore up to Book {book}, Chapter {chapter} for '{series_name}':\n\n- " + "\n- ".join(lore_entries)

def search_lore(term):
    lore_db = load_lore()
    matches = []
    term_lower = term.lower()

    for series, books in lore_db.items():
        for book, chapters in books.items():
            for chap, text in chapters.items():
                if term_lower in text.lower():
                    matches.append(f"[{series}] Book {book}, Chapter {chap}: {text}")

    if not matches:
        return f"[Archie] 🔍 No mentions of '{term}' found in available lore."

    return f"[Archie] Results for '{term}':\n\n- " + "\n- ".join(matches)

def print_help():
    print("[Archie] Usage:")
    print("  python lore_engine.py update <series> <book_number> <chapter>")
    print("  python lore_engine.py lore <series>")
    print("  python lore_engine.py search <term>")
    print("  python lore_engine.py help")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print_help()
        sys.exit(1)

    command = sys.argv[1].lower()

    if command == "update" and len(sys.argv) == 5:
        update_progress(sys.argv[2], int(sys.argv[3]), int(sys.argv[4]))
    elif command == "lore" and len(sys.argv) == 3:
        print(get_lore(sys.argv[2]))
    elif command == "search" and len(sys.argv) == 3:
        print(search_lore(sys.argv[2]))
    elif command == "help":
        print_help()
    else:
        print("[Archie] ⚠️ Invalid command. Use 'help' to see available options.")
















