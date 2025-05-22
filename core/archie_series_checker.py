
import os
import json
import requests
from bs4 import BeautifulSoup
from collections import defaultdict
import time

CATALOG_FILE = "book_status.json"
STATUS_FILE = "series_status.json"
FLAGGED_FILE = "flagged_authors.json"

def load_catalog():
    if os.path.exists(CATALOG_FILE):
        with open(CATALOG_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def load_series_status():
    if os.path.exists(STATUS_FILE):
        with open(STATUS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_series_status(data):
    with open(STATUS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def search_goodreads_series(series_name):
    query = f"{series_name} site:goodreads.com/series"
    headers = {"User-Agent": "Mozilla/5.0"}
    url = f"https://www.google.com/search?q={requests.utils.quote(query)}"
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return None

    soup = BeautifulSoup(response.text, "html.parser")
    links = soup.select("a")
    for link in links:
        href = link.get("href", "")
        if "goodreads.com/series/" in href:
            start = href.find("http")
            end = href.find("&", start)
            return href[start:end]
    return None

def get_goodreads_series_books(series_url):
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(series_url, headers=headers)
    if response.status_code != 200:
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    books = []
    for div in soup.select(".bookTitle"):
        title = div.get_text(strip=True)
        books.append(title)
    return books

def compare_books(owned, official_titles):
    owned_titles = {b["title"].lower() for b in owned}
    missing = [title for title in official_titles if title.lower() not in owned_titles]
    return missing

def archie_series_checker():
    catalog = load_catalog()
    existing_status = load_series_status()
    already_checked = {entry["series"] for entry in existing_status}

    series_by_author = defaultdict(lambda: defaultdict(list))

    for book in catalog:
        author = book.get("author")
        series = book.get("series")
        if author and series:
            series_by_author[author][series].append(book)

    new_results = []

    for author, series_map in series_by_author.items():
        print(f"\n🕵️ Archie is now checking: {author}")
        for series, books in series_map.items():
            if series in already_checked:
                print(f"  ⏩ Already checked '{series}', skipping.")
                continue

            print(f"  🔍 Series: {series}")
            series_url = search_goodreads_series(series)
            if not series_url:
                print(f"  ⚠️ Could not find Goodreads page for '{series}'")
                continue

            official_titles = get_goodreads_series_books(series_url)
            if not official_titles:
                print(f"  ⚠️ Could not retrieve book list for '{series}'")
                continue

            missing = compare_books(books, official_titles)
            status = "complete" if not missing else "incomplete"

            entry = {
                "author": author,
                "series": series,
                "status": status,
                "owned": len(books),
                "official_total": len(official_titles),
                "missing_titles": missing,
                "goodreads_url": series_url
            }
            new_results.append(entry)
            existing_status.append(entry)

            if status != "complete":
                print(f"  ⚠️ Missing books: {missing}")
            else:
                print("  ✅ Series complete!")

            time.sleep(2)  # Respectful delay

    save_series_status(existing_status)
    print(f"\n✅ Archie finished checking {len(new_results)} new series.")
    return new_results

if __name__ == "__main__":
    archie_series_checker()
