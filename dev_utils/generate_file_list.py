import os
import json

# Set path to Bookshelf (sync'ed inside eBooksCharlie)
BOOKSHELF_PATH = os.path.expanduser(
    "~/Library/CloudStorage/GoogleDrive-geoford85@gmail.com/My Drive/eBooksCharlie/Bookshelf"
)

# Supported eBook extensions
ebook_extensions = {'.epub', '.mobi', '.azw3', '.pdf'}

# List to hold file data
file_list = []

for root, dirs, files in os.walk(BOOKSHELF_PATH):
    for file in files:
        ext = os.path.splitext(file)[1].lower()
        if ext in ebook_extensions:
            full_path = os.path.join(root, file)
            relative_path = os.path.relpath(full_path, BOOKSHELF_PATH)
            file_list.append({
                "file_name": file,
                "relative_path": relative_path,
                "format": ext.strip(".")
            })

# Output to JSON
output_file = os.path.expanduser("~/Desktop/book_file_list.json")
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(file_list, f, indent=2)

print(f"✅ File list saved to {output_file}")

