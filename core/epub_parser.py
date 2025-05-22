# ~/Desktop/archives/epub_parser.py

from ebooklib import epub
import os
from config import LIBRARY_PATH

def extract_epub_metadata(filename_or_path):
    # If the file is just a name, join it with LIBRARY_PATH
    file_path = filename_or_path
    if not os.path.isabs(filename_or_path):
        file_path = os.path.join(LIBRARY_PATH, filename_or_path)

    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"No such file: {file_path}")
    if not file_path.lower().endswith(".epub"):
        raise ValueError("Provided file is not an EPUB.")

    book = epub.read_epub(file_path)

    metadata = {
        "title": None,
        "authors": [],
        "language": None,
        "identifiers": {},
        "file_name": os.path.basename(file_path),
        "file_path": os.path.abspath(file_path)
    }

    # Title
    title = book.get_metadata("DC", "title")
    if title:
        metadata["title"] = title[0][0]

    # Authors
    authors = book.get_metadata("DC", "creator")
    if authors:
        metadata["authors"] = [a[0] for a in authors]

    # Language
    language = book.get_metadata("DC", "language")
    if language:
        metadata["language"] = language[0][0]

    # Identifiers (like ISBN, UUID, etc.)
    identifiers = book.get_metadata("DC", "identifier")
    if identifiers:
        for ident in identifiers:
            if len(ident) >= 1:
                value = ident[0]
                scheme = ident[1].get("id") if isinstance(ident[1], dict) else None
                if scheme:
                    metadata["identifiers"][scheme] = value
                else:
                    metadata["identifiers"][f"id_{len(metadata['identifiers'])+1}"] = value

    return metadata

