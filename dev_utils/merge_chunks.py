# ~/Desktop/archives/merge_chunks.py

import json
import os

# Change this list to match the number of parts you saved
chunk_files = [
    "library_catalog_part1.json",
    "library_catalog_part2.json",
    "library_catalog_part3.json",
    # Add more here if needed
]

merged_data = []

for filename in chunk_files:
    file_path = os.path.join(os.getcwd(), filename)
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            try:
                chunk = json.load(f)
                if isinstance(chunk, list):
                    merged_data.extend(chunk)
                else:
                    print(f"⚠️ Skipping {filename} — Not a JSON array.")
            except json.JSONDecodeError as e:
                print(f"❌ Error parsing {filename}: {e}")
    else:
        print(f"🚫 File not found: {filename}")

# Save the full merged catalog
output_path = os.path.join(os.getcwd(), "library_catalog.json")

with open(output_path, "w", encoding="utf-8") as out_file:
    json.dump(merged_data, out_file, indent=2, ensure_ascii=False)

print(f"✅ Merged {len(chunk_files)} chunk(s) into library_catalog.json with {len(merged_data)} entries.")

