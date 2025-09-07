from django.http import HttpResponse
from django.views.generic import DetailView
from .models import Book, Library

# --- Function-based view: list all books ---
def list_books(request):
    # Plain-text output (meets the task requirement)
    books = Book.objects.select_related("author").all()
    lines = [f"{b.title} by {b.author.name}" for b in books]
    return HttpResponse("\n".join(lines), content_type="text/plain")

    # If you prefer HTML later, switch to:
    # from django.shortcuts import render
    # return render(request, "relationship_app/list_books.html", {"books": books})

# --- Class-based view: details for a specific library ---
class LibraryDetailView(DetailView):
    model = Library
    template_name = "relationship_app/library_detail.html"  # used if you add the template
    context_object_name = "library"
    # DetailView expects <int:pk> in the URL by default
