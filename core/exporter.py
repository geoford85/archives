# ~/Desktop/archives/exporter.py

import os
import json
import csv

EXPORTS_DIR = "exports"

def ensure_export_folder():
    if not os.path.exists(EXPORTS_DIR):
        os.makedirs(EXPORTS_DIR)

def export_json_to_csv(json_file, output_name, fields):
    if not os.path.exists(json_file):
        print(f"❌ File not found: {json_file}")
        return

    with open(json_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    # If it's a dict, convert to list
    if isinstance(data, dict):
        data = [v for _, v in data.items()]

    with open(os.path.join(EXPORTS_DIR, output_name), "w", encoding="utf-8", newline='') as out_csv:
        writer = csv.DictWriter(out_csv, fieldnames=fields)
        writer.writeheader()
        for row in data:
            writer.writerow({k: row.get(k, "") for k in fields})

    print(f"✅ Exported {output_name}")

def run_exports():
    ensure_export_folder()

    export_json_to_csv(
        "library_catalog.json",
        "library_catalog.csv",
        ["title", "author", "series", "series_number", "format", "file_path", "id"]
    )

    export_json_to_csv(
        "book_status.json",
        "book_status.csv",
        ["title", "status", "last_updated"]
    )

    export_json_to_csv(
        "reading_progress.json",
        "reading_progress.csv",
        ["title", "series", "last_location", "last_updated"]
    )

    export_json_to_csv(
        "reading_log.json",
        "reading_log.csv",
        ["title", "author", "series", "date_finished"]
    )

if __name__ == "__main__":
    run_exports()

