
import json
import os

GLOSSARY_FILE = "lore_glossary.json"

def load_glossary():
    if os.path.exists(GLOSSARY_FILE):
        with open(GLOSSARY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def get_lore_entry(term):
    glossary = load_glossary()
    if not glossary:
        return "⚠️ Lore glossary not found or empty."

    term_lower = term.lower()
    for key, value in glossary.items():
        if term_lower == key.lower():
            return f"📚 {key}:
{value}"

    return f"🔍 No lore found for '{term}'. Try another name, place, or object."
