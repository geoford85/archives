# ~/Desktop/archives/lorekeeper.py

import json
import os

STATUS_FILE = "book_status.json"
SUMMARY_STORE = "lore_summaries.json"

def load_status():
    if os.path.exists(STATUS_FILE):
        with open(STATUS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def load_summaries():
    if os.path.exists(SUMMARY_STORE):
        with open(SUMMARY_STORE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def get_summary(book_id):
    status = load_status()
    summaries = load_summaries()

    book_info = status.get(book_id)

    if not book_info:
        print("⚠️ No status found for this book.")
        return

    if book_info["status"] != "read":
        print("🙅 Spoiler shield activated! You haven’t finished this one yet.")
        return

    summary = summaries.get(book_id)
    if summary:
        print(f"📖 Summary for '{book_info['title']}':\n{summary}")
    else:
        print("📘 No summary stored yet for this book.")

def store_summary(book_id, text):
    summaries = load_summaries()
    summaries[book_id] = text
    with open(SUMMARY_STORE, "w", encoding="utf-8") as f:
        json.dump(summaries, f, indent=2, ensure_ascii=False)
    print("✅ Summary saved.")

# Example: Add and retrieve summary
if __name__ == "__main__":
    # Store a fake summary for testing
    store_summary(
        book_id="abc123xyz",
        text="A powerful sacred artist enters a tournament and learns the cost of holding back."
    )

    # Retrieve it (assuming you've marked it as read in book_status.json)
    get_summary("abc123xyz")

