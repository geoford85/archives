
import os
import json
from collections import defaultdict

BOOKS_FILE = "book_status.json"
SERIES_FILE = "series_status.json"
RECOMMENDATIONS_FILE = "recommendations_by_author.json"

def load_json_file(path):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def build_recommendations():
    books = load_json_file(BOOKS_FILE)
    series_status = load_json_file(SERIES_FILE)

    owned_titles = {book["title"].lower(): book for book in books}
    author_series_map = defaultdict(lambda: {"owned_series": set(), "owned_titles": set(), "recs": []})

    for book in books:
        author = book.get("author")
        title = book.get("title")
        series = book.get("series")

        if not author or not title:
            continue

        author_series_map[author]["owned_titles"].add(title.lower())
        if series:
            author_series_map[author]["owned_series"].add(series)

    # Match missing or related series from series_status
    for entry in series_status:
        author = entry.get("author")
        series = entry.get("series")
        missing = entry.get("missing_titles", [])

        if not author or not series or not missing:
            continue

        rec = {
            "series": series,
            "missing_titles": missing,
            "status": entry.get("status", "incomplete"),
            "goodreads_url": entry.get("goodreads_url")
        }

        if series not in author_series_map[author]["owned_series"]:
            author_series_map[author]["recs"].append(rec)

    # Save formatted output
    final_output = []
    for author, data in author_series_map.items():
        if data["recs"]:
            final_output.append({
                "author": author,
                "owned_series": sorted(data["owned_series"]),
                "recommended_series": data["recs"]
            })

    with open(RECOMMENDATIONS_FILE, "w", encoding="utf-8") as f:
        json.dump(final_output, f, indent=2)

    print(f"✅ Recommendations saved to {RECOMMENDATIONS_FILE} for {len(final_output)} authors.")

if __name__ == "__main__":
    build_recommendations()
