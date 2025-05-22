
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

from recommend_handler import get_recommendations
from lore_handler import get_lore_entry
from search_handler import search_metadata
from whiskerly_picker import whiskerly_suggest
from archie_series_checker import archie_series_checker
from generate_recommendations import build_recommendations
from progress_handler import get_progress, update_progress
from log_handler import add_log_entry, get_log

import json
import os

BOOKS_FILE = "book_status.json"
SERIES_FILE = "series_status.json"
RECS_FILE = "recommendations_by_author.json"

app = Flask(__name__)
CORS(app)

def load_json(path):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

@app.route("/")
def homepage():
    return send_from_directory(".", "index.html")

@app.route("/api/message", methods=["POST"])
def handle_message():
    user_input = request.json.get("message", "")
    response = interpret_command(user_input)
    return jsonify(reply=response)

@app.route("/api/whiskerly", methods=["GET"])
def whiskerly_route():
    mood = request.args.get("mood", None)
    result = whiskerly_suggest(mood)
    return jsonify(result)

@app.route("/api/recommend", methods=["GET"])
def recommend_route():
    author = request.args.get("author")
    result = get_recommendations(author)
    return jsonify({"result": result})

@app.route("/api/lore", methods=["GET"])
def lore_route():
    term = request.args.get("term")
    result = get_lore_entry(term)
    return jsonify({"result": result})

@app.route("/api/search", methods=["GET"])
def search_route():
    query = request.args.get("q")
    result = search_metadata(query)
    return jsonify({"result": result})

@app.route("/api/progress", methods=["GET", "POST"])
def progress_route():
    if request.method == "GET":
        title = request.args.get("book", "")
        result = get_progress(title)
    else:
        data = request.json or {}
        result = update_progress(data.get("book", ""), data.get("location", ""))
    return jsonify({"result": result})

@app.route("/api/log", methods=["GET", "POST"])
def log_route():
    if request.method == "GET":
        result = get_log()
    else:
        data = request.json or {}
        result = add_log_entry(data.get("entry", ""))
    return jsonify({"result": result})

def interpret_command(user_input):
    user_input = user_input.strip()

    if user_input.lower().startswith("missing "):
        author = user_input[8:].strip()
        return list_missing_series_by_author(author)

    elif user_input.lower().startswith("recommend "):
        author = user_input[10:].strip()
        return get_recommendations(author)

    elif user_input.lower().startswith("lore "):
        term = user_input[5:].strip()
        return get_lore_entry(term)

    elif user_input.lower().startswith("search "):
        term = user_input[7:].strip()
        return search_metadata(term)

    elif user_input.lower().startswith("progress "):
        _, book, _, location = user_input.partition("-")
        return update_progress(book.strip(), location.strip())

    elif user_input.lower().startswith("log "):
        return add_log_entry(user_input[4:].strip())

    elif user_input.lower() in ["refresh", "update all", "rescan"]:
        archie_series_checker()
        build_recommendations()
        return "🔄 Archie has refreshed his records."

    elif user_input.lower() in ["hello", "hi", "yo", "hey"]:
        return "👋 Hello! I'm Archie. Ask about missing books, lore, or say 'recommend [author]'."

    return "🤔 I didn’t understand that. Try 'recommend [author]', 'lore [term]', or 'search [word]'."

def list_missing_series_by_author(author_name):
    series_data = load_json(SERIES_FILE)
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

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
