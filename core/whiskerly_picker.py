
import json
import os
import random

BOOKS_FILE = "book_status.json"

# Sample Whiskerly quotes
QUOTES = [
    "Go on, give it a try. I have *excellent* taste.",
    "This one's been gathering digital dust, George.",
    "I picked this with one paw and half a brain tied behind my back.",
    "Read it or I start knocking books off your shelves.",
    "I don’t make the rules—wait, yes I do. Read this.",
    "It’s this or another reread of The Hobbit. Your call."
]

def load_books():
    if not os.path.exists(BOOKS_FILE):
        return []
    with open(BOOKS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def whiskerly_suggest(mood=None):
    books = load_books()
    if not books:
        return {"error": "No books found in book_status.json"}

    # Filter to "to be read" books if a 'status' field exists
    unread = [b for b in books if b.get("status", "").lower() != "read"]

    if mood:
        mood = mood.lower()
        unread = [b for b in unread if mood in b.get("title", "").lower() or mood in b.get("series", "").lower()]

    if not unread:
        return {"message": "Couldn't find any unread books matching that mood. Try a broader vibe?"}

    pick = random.choice(unread)
    return {
        "title": pick.get("title", "Unknown Title"),
        "author": pick.get("author", "Unknown Author"),
        "series": pick.get("series", "Standalone"),
        "quote": random.choice(QUOTES)
    }

# If run directly
if __name__ == "__main__":
    result = whiskerly_suggest()
    print(f"🐾 Whiskerly Suggests: {result['title']} by {result['author']}")
    if result.get("series"):
        print(f"  Series: {result['series']}")
    print(f"  💬 {result['quote']}")
