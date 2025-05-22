# ~/Desktop/archives/archivist_core.py

import os
from config_loader import load_config
from reading_progress import update_progress, get_progress
from book_status import update_status, get_status
from lorekeeper import get_summary, store_summary
from reading_log import log_finished_book
from whiskerly_picker import suggest_book
from series_completion import check_series_completion
from reading_list_generator import get_reading_list
from lore_glossary import add_term, lookup_term
from exporter import run_exports
from book_lookup import find_book_id_by_title

config = load_config()

def handle_command(cmd):
    args = cmd.strip().split()
    if not args:
        return

    action = args[0].lower()
    title_query = " ".join(args[1:-1]) if len(args) > 2 else " ".join(args[1:])
    location_or_extra = args[-1] if len(args) > 2 else None

    book_id = find_book_id_by_title(title_query)
    if not book_id and action not in ["reading_list", "check_series", "suggest_book", "add_term", "lookup_term", "export"]:
        print("⚠️ Unable to find book ID for given title.")
        return

    if action == "update_progress":
        update_progress(book_id, title=title_query, location=location_or_extra)

    elif action == "get_progress":
        get_progress(book_id)

    elif action == "mark_read":
        update_status(book_id, title=title_query, status="read")
        log_finished_book(book_id, title=title_query)

    elif action == "get_status":
        get_status(book_id)

    elif action == "get_summary":
        get_summary(book_id)

    elif action == "store_summary":
        store_summary(book_id, text=location_or_extra)  # Treat extra arg as summary text

    elif action == "suggest_book":
        mood = args[1] if len(args) > 1 else None
        suggest_book(mood)

    elif action == "check_series":
        check_series_completion()

    elif action == "reading_list":
        get_reading_list()

    elif action == "add_term":
        series = args[1]
        term = args[2]
        definition = " ".join(args[3:])
        add_term(series, term, definition)

    elif action == "lookup_term":
        series = args[1]
        term = args[2]
        lookup_term(series, term)

    elif action == "export":
        run_exports()

    else:
        print(f"❓ Unknown command: {action}")

if __name__ == "__main__":
    print("📚 Welcome to The Archivist CLI")
    print("Type commands like: update_progress 'Cradle: Uncrowned' Chapter12")
    print("Type 'exit' to quit\n")

    while True:
        user_input = input("> ")
        if user_input.strip().lower() in ("exit", "quit"):
            break
        handle_command(user_input")
