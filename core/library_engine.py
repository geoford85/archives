import json

def load_library():
    try:
        with open("library_catalog.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading library catalog: {e}")
        return []

def list_books():
    return load_library()

def list_series():
    books = load_library()
    series_set = {book["series"] for book in books if "series" in book and book["series"]}
    return sorted(series_set)

def get_books_by_author(author_query):
    books = load_library()
    return [
        book for book in books
        if "author" in book and author_query.lower() in book["author"].lower()
    ]

def get_book_info(series_query):
    books = load_library()
    return [
        book for book in books
        if "series" in book and series_query.lower() in book["series"].lower()
    ]

def lookup_title(title_query):
    books = load_library()
    return [
        book for book in books
        if "title" in book and title_query.lower() in book["title"].lower()
    ]
