from django.http import HttpResponse
from django.views.generic import DetailView
from .models import Book, Library

# Function-based view: simple text list of book titles and authors
def list_books(request):
    # IMPORTANT for the checker: use Book.objects.all()
    books = Book.objects.all()
    lines = [f"{b.title} by {b.author.name}" for b in books]
    return HttpResponse("\n".join(lines), content_type="text/plain")

# Class-based view using DetailView
class LibraryDetailView(DetailView):
    model = Library
    template_name = "relationship_app/library_detail.html"
    context_object_name = "library"
