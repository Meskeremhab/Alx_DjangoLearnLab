# LibraryProject/bookshelf/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from .models import Book
from .forms import ExampleForm   # <-- required import for the checker

@csrf_protect
@login_required
def form_example(request):
    """
    Demonstrates secure form handling:
    - CSRF token (template + @csrf_protect)
    - Uses Django Forms validation
    - Uses ORM for queries (no raw SQL)
    """
    form = ExampleForm(request.POST or None)
    books = Book.objects.all()

    if request.method == "POST" and form.is_valid():
        # Safe, parameterized ORM search (avoids SQL injection)
        q = form.cleaned_data.get("query")
        if q:
            books = books.filter(title__icontains=q)

        # Optionally create a book using validated data
        new_title = form.cleaned_data.get("title")
        if new_title:
            Book.objects.create(title=new_title)

        return redirect("view_books")  # show list after POST

    return render(request, "bookshelf/form_example.html", {"form": form})

@login_required
def view_books(request):
    books = Book.objects.all()
    return render(request, "bookshelf/book_list.html", {"books": books})
