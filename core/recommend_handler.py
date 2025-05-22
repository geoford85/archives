
import json
import os

RECS_FILE = "recommendations_by_author.json"

def load_recs():
    if os.path.exists(RECS_FILE):
        with open(RECS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def get_recommendations(author=None):
    recs = load_recs()
    if not recs:
        return "⚠️ No recommendations found. Try running the update command first."

    if author:
        filtered = [r for r in recs if r["author"].lower() == author.lower()]
        if not filtered:
            return f"🤷‍♂️ No recommendations found for '{author}'."
        return format_recommendations(filtered)

    # If no author is specified, return a summary from all
    return format_recommendations(recs[:5])

def format_recommendations(entries):
    output = []
    for entry in entries:
        output.append(f"📖 {entry['author']}")
        for series in entry.get("recommended_series", []):
            status = series.get("status", "unknown")
            missing = series.get("missing_titles", [])
            line = f"  - {series['series']}: {status}"
            if missing:
                line += f" (Missing: {', '.join(missing)})"
            output.append(line)
        output.append("")  # blank line
    return "\n".join(output).strip()
