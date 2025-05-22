import os
import json

# Updated to support both list-style and dict-style JSON
author_folder = os.path.expanduser("~/Desktop/library/Parsed Authors and Universes")

master_catalog = []

for filename in os.listdir(author_folder):
    if filename.endswith(".json"):
        full_path = os.path.join(author_folder, filename)
        try:
            with open(full_path, "r", encoding="utf-8") as f:
                data = json.load(f)

                if isinstance(data, list):
                    master_catalog.extend(data)
                elif isinstance(data, dict) and "books" in data and isinstance(data["books"], list):
                    master_catalog.extend(data["books"])
                else:
                    print(f"⚠️  Skipping {filename} — unexpected format.")

        except Exception as e:
            print(f"❌ Error reading {filename}: {e}")

# Output merged file
output_path = "book_status.json"
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(master_catalog, f, indent=2)

print(f"✅ Merged catalog saved to {output_path} with {len(master_catalog)} books.")

