# ~/Desktop/archives/lore_glossary.py

import json
import os

GLOSSARY_FILE = "lore_glossary.json"

def load_glossary():
    if os.path.exists(GLOSSARY_FILE):
        with open(GLOSSARY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_glossary(data):
    with open(GLOSSARY_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def add_term(series, term, definition):
    glossary = load_glossary()

    if series not in glossary:
        glossary[series] = {}

    glossary[series][term] = definition
    save_glossary(glossary)
    print(f"📖 Added term '{term}' under '{series}'.")

def lookup_term(series, term):
    glossary = load_glossary()

    series_terms = glossary.get(series)
    if not series_terms:
        print(f"❌ No glossary found for series: {series}")
        return

    result = series_terms.get(term)
    if result:
        print(f"📘 {term}: {result}")
    else:
        print(f"❓ No entry for '{term}' in '{series}' glossary.")

# Example usage
if __name__ == "__main__":
    # Add a term
    add_term(
        series="Cradle",
        term="Orthos",
        definition="A talking, fire-breathing turtle companion of Lindon. Surprisingly sassy."
    )

    # Lookup a term
    lookup_term("Cradle", "Orthos")

