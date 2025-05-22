
import json
import os

BOOKS_FILE = "book_status.json"

def load_books():
    if os.path.exists(BOOKS_FILE):
        with open(BOOKS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def search_metadata(query):
    if not query:
        return "🔍 Please enter something to search for."

    books = load_books()
    if not books:
        return "⚠️ No books found in the catalog."

    query = query.lower()
    results = []

    for book in books:
        title = book.get("title", "").lower()
        author = book.get("author", "").lower()
        series = book.get("series", "").lower()

        if query in title or query in author or query in series:
            result = f"📘 {book.get('title', 'Unknown')} by {book.get('author', 'Unknown')}"
            if series:
                result += f"  [{series}]"
            results.append(result)

    if not results:
        return f"🤔 No results found for '{query}'."

    return "\n".join(results[:25])
