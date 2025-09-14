# LibraryProject/bookshelf/views.py
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import permission_required, login_required
from django.http import HttpResponseForbidden
from .models import Book

@login_required
@permission_required('bookshelf.can_view', raise_exception=True)
def view_books(request):
    books = Book.objects.all()
    return render(request, 'bookshelf/book_list.html', {"books": books})

@login_required
@permission_required('bookshelf.can_create', raise_exception=True)
def create_book(request):
    if request.method == "POST":
        title = request.POST.get("title") or "Untitled"
        author = request.POST.get("author") or ""
        Book.objects.create(title=title, author=author)
        return redirect('view_books')
    return render(request, 'bookshelf/book_form.html')

@login_required
@permission_required('bookshelf.can_edit', raise_exception=True)
def edit_book(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    if request.method == "POST":
        book.title = request.POST.get("title") or book.title
        book.author = request.POST.get("author") or book.author
        book.save()
        return redirect('view_books')
    return render(request, 'bookshelf/book_form.html', {"book": book})

@login_required
@permission_required('bookshelf.can_delete', raise_exception=True)
def delete_book(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    if request.method == "POST":
        book.delete()
        return redirect('view_books')
    # simple confirmation page or forbid GET deletes
    return render(request, 'bookshelf/book_confirm_delete.html', {"book": book})
