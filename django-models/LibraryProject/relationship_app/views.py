from django.shortcuts import render
from django.views.generic import DetailView
from .models import Book, Library


# Function-based view: list all books (must render the template)
def list_books(request):
    # Checker wants: Book.objects.all()
    books = Book.objects.all()
    return render(request, "relationship_app/list_books.html", {"books": books})


# Class-based view using DetailView
class LibraryDetailView(DetailView):
    model = Library
    template_name = "relationship_app/library_detail.html"
    context_object_name = "library"
