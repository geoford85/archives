import os
import json

# 📍 Set this to your actual eBooksCharlie path
ROOT_DIR = "/Users/gford/Library/CloudStorage/GoogleDrive-geoford85@gmail.com/My Drive/eBooksCharlie"

# 🧾 List of all book file formats we care about
BOOK_EXTENSIONS = (
    ".epub", ".mobi", ".pdf", ".azw3", ".azw", ".docx", ".txt",
    ".fb2", ".lit", ".rtf", ".djvu", ".html", ".htm",
    ".cbz", ".cbr", ".ibooks"
)

library_entries = []

for root, dirs, files in os.walk(ROOT_DIR):
    for file in files:
        if file.lower().endswith(BOOK_EXTENSIONS):
            full_path = os.path.join(root, file)
            rel_path = os.path.relpath(full_path, ROOT_DIR)
            author = os.path.basename(os.path.dirname(full_path))

            entry = {
                "author_folder": author,
                "file_name": file,
                "relative_path": rel_path
            }
            library_entries.append(entry)

# 💾 Save to file
with open("library_snapshot_full.json", "w") as f:
    json.dump(library_entries, f, indent=2)

print(f"✅ Scanned {len(library_entries)} books. Saved to library_snapshot_full.json.")

