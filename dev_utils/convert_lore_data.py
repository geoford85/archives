import json

with open("lore_data.json", "r") as f:
    raw = json.load(f)

converted = []

for series, books in raw.items():
    for book_num, chapters in books.items():
        for chapter_num, summary in chapters.items():
            converted.append({
                "series": series,
                "book": int(book_num),
                "chapter": int(chapter_num),
                "summary": summary
            })

with open("lore_data.json", "w") as f:
    json.dump(converted, f, indent=2)

print("✅ lore_data.json has been converted for Archie!")

