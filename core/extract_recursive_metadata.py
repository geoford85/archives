import json

INPUT_FILE = "ebook_file_list.json"
OUTPUT_FILE = "library_catalog.json"

def extract_ebook_metadata():
    with open(INPUT_FILE, "r") as infile:
        data = json.load(infile)

    ebooks = []
    for entry in data:
        # Normalize format based on mimeType
        mime = entry.get("mimeType", "").lower()
        if mime.startswith("application/epub") or mime.endswith((".epub", ".mobi", ".azw3", ".pdf")):
            ext = ".epub" if "epub" in mime else ".mobi"
        else:
            continue

        ebooks.append({
            "title": entry.get("title", ""),
            "path": entry.get("path", ""),
            "format": ext,
            "id": entry.get("id", "")
        })

    with open(OUTPUT_FILE, "w") as outfile:
        json.dump(ebooks, outfile, indent=2)

    print(f"✅ Extracted {len(ebooks)} ebook entries.")

if __name__ == "__main__":
    extract_ebook_metadata()

