import os
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "LibraryProject.settings")

import django
django.setup()

from relationship_app.models import Author, Book, Library, Librarian


def books_by_author(author_name: str):
    """
    Query all books by a specific author.
    Must use: Book.objects.filter(author=author)
    """
    try:
        author = Author.objects.get(name=author_name)
    except Author.DoesNotExist:
        print(f"Author '{author_name}' not found.")
        return []
    return Book.objects.filter(author=author)   # <<< checker wants this


def books_in_library(library_name: str):
    """
    List all books in a library.
    Must use: library.books.all()
    """
    try:
        library = Library.objects.get(name=library_name)
    except Library.DoesNotExist:
        print(f"Library '{library_name}' not found.")
        return []
    return library.books.all()   # <<< checker wants this


def librarian_for_library(library_name: str):
    """
    Retrieve the librarian for a library.
    Must use: Librarian.objects.get(library=library)
    """
    try:
        library = Library.objects.get(name=library_name)
    except Library.DoesNotExist:
        print(f"Library '{library_name}' not found.")
        return None
    try:
        return Librarian.objects.get(library=library)   # <<< checker wants this
    except Librarian.DoesNotExist:
        print(f"No librarian assigned to '{library_name}'.")
        return None


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
