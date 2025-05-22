import requests
from bs4 import BeautifulSoup
import json
import os
from collections import defaultdict
import time

CATALOG_FILE = "book_status.json"
OUTPUT_FILE = "series_status.json"

def load_catalog():
    if os.path.exists(CATALOG_FILE):
        with open(CATALOG_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def group_books_by_series(catalog):
    series_books = defaultdict(list)
    for book in catalog:
        series = book.get("series")
        if series:
            series_books[series].append(book)
    return series_books

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

def compare_series(owned_books, official_titles):
    owned_titles = {b["title"].lower() for b in owned_books}
    missing = [title for title in official_titles if title.lower() not in owned_titles]
    return missing

def check_series_completion_with_goodreads():
    catalog = load_catalog()
    series_books = group_books_by_series(catalog)

    results = []

    for series, books in series_books.items():
        print(f"🔍 Checking series: {series}")
        series_url = search_goodreads_series(series)
        if not series_url:
            print(f"⚠️ Could not find Goodreads page for '{series}'")
            continue

        print(f"🌐 Goodreads URL: {series_url}")
        official_titles = get_goodreads_series_books(series_url)
        if not official_titles:
            print(f"⚠️ Could not retrieve book list for '{series}'")
            continue

        missing = compare_series(books, official_titles)
        status = "complete" if not missing else "incomplete"

        results.append({
            "series": series,
            "status": status,
            "owned": len(books),
            "official_total": len(official_titles),
            "missing_titles": missing,
            "goodreads_url": series_url
        })

        time.sleep(2)  # Be nice to Goodreads

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

    print(f"\n✅ Full series scan complete. Results saved to {OUTPUT_FILE}")
    print(f"📚 {len(results)} series analyzed.\n")

if __name__ == "__main__":
    check_series_completion_with_goodreads()

