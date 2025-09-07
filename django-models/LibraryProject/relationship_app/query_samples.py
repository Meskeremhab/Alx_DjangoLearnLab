# relationship_app/query_samples.py

import os
import sys
from pathlib import Path

# Make sure Python can import the "LibraryProject" package (sibling to this folder)
BASE_DIR = Path(__file__).resolve().parent.parent  # ...\LibraryProject
sys.path.insert(0, str(BASE_DIR))

# Configure Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "LibraryProject.settings")

import django
django.setup()

from relationship_app.models import Author, Book, Library


def books_by_author(author_name: str):
    try:
        author = Author.objects.get(name=author_name)
    except Author.DoesNotExist:
        print(f"Author '{author_name}' not found.")
        return []
    return list(author.books.all().only("id", "title"))


def books_in_library(library_name: str):
    try:
        library = Library.objects.get(name=library_name)
    except Library.DoesNotExist:
        print(f"Library '{library_name}' not found.")
        return []
    return list(library.books.all().select_related("author").only("id", "title", "author__name"))


def librarian_for_library(library_name: str):
    try:
        library = Library.objects.get(name=library_name)
    except Library.DoesNotExist:
        print(f"Library '{library_name}' not found.")
        return None
    return getattr(library, "librarian", None)


if __name__ == "__main__":
    author_name = "Toni Morrison"
    library_name = "Central Library"

    print(f"\nBooks by {author_name}:")
    for b in books_by_author(author_name):
        print(f"- {b.title}")

    print(f"\nBooks in {library_name}:")
    for b in books_in_library(library_name):
        print(f"- {b.title} (by {b.author.name})")

    print(f"\nLibrarian for {library_name}:")
    lb = librarian_for_library(library_name)
    if lb:
        print(f"- {lb.name}")
    else:
        print("- None assigned")
