from bookshelf.models import Book
book = Book.objects.get(title="1984", author="George Orwell", publication_year=1949)
(book.title, book.author, book.publication_year)  # ('1984', 'George Orwell', 1949)
