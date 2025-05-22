
import json
import os

BOOKS_FILE = "book_status.json"
SERIES_FILE = "series_status.json"
RECS_FILE = "recommendations_by_author.json"

def load_json(path):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def list_missing_series_by_author(author_name, series_data):
    results = [entry for entry in series_data if entry.get("author", "").lower() == author_name.lower()]
    if not results:
        return f"🤷‍♂️ No series found for '{author_name}'. Try a different name."

    response = []
    for entry in results:
        missing = entry.get("missing_titles", [])
        if missing:
            response.append(f"📚 *{entry['series']}* — missing: {', '.join(missing)}")
        else:
            response.append(f"✅ *{entry['series']}* — complete.")
    return "\n".join(response)

def get_recommendations_by_author(author_name, recs_data):
    recs = [r for r in recs_data if r["author"].lower() == author_name.lower()]
    if not recs:
        return f"🤔 No recommendations found yet for '{author_name}'."

    out = []
    for r in recs:
        for s in r.get("recommended_series", []):
            line = f"🌟 *{s['series']}* — {s['status']}, missing: {', '.join(s['missing_titles'])}"
            out.append(line)
    return "\n".join(out) if out else f"✅ Looks like you’ve got everything from {author_name}!"

def main():
    print("🧙 Welcome to Archie, your friendly bookish assistant.")
    print("Type 'missing [author]', 'recommend [author]', or 'exit' to leave.")

    books = load_json(BOOKS_FILE)
    series = load_json(SERIES_FILE)
    recs = load_json(RECS_FILE)

    while True:
        user_input = input("> ").strip()
        if user_input.lower() in ("exit", "quit"):
            print("📚 Farewell. I'll be reorganizing the scrolls while you're away.")
            break

        if user_input.lower().startswith("missing "):
            author = user_input[8:].strip()
            print(list_missing_series_by_author(author, series))
        elif user_input.lower().startswith("recommend "):
            author = user_input[10:].strip()
            print(get_recommendations_by_author(author, recs))
        else:
            print("❓ I didn’t understand that. Try 'missing [author]' or 'recommend [author]'.")

if __name__ == "__main__":
    main()
