import json

CATALOG_FILE = "library_catalog.json"

def load_catalog():
    with open(CATALOG_FILE, "r") as f:
        return json.load(f)

def get_books_by_author(author_name):
    catalog = load_catalog()
    books = []
    for entry in catalog:
        if entry.get("author", "").lower() == author_name.lower():
            books.append(entry.get("title", "Unknown Title"))
    if not books:
        return f"🤷‍♂️ No books found by '{author_name}'—maybe a typo? Or Whiskerly ate the label."
    return "📚 Books by " + author_name + ":\n" + "\n".join(f"- {b}" for b in books)

def get_book_info(series_name):
    catalog = load_catalog()
    books = []
    for entry in catalog:
        if entry.get("series", "").lower() == series_name.lower():
            title = entry.get("title", "Unknown Title")
            author = entry.get("author", "Unknown")
            books.append(f"{title} by {author}")
    if not books:
        return f"🤔 I couldn’t find anything called '{series_name}' in the archives."
    return f"📘 Info for '{series_name}':\n" + "\n".join(f"- {b}" for b in books)

