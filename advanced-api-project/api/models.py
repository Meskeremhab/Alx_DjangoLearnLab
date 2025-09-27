from django.db import models

# Create your models here.
class Author(models.Model):
    """
    Represents a writer who can have many books.

    Fields:
        name: Human-readable name of the author.
    Relationships:
        Book.author (FK) points back to Author with related_name='books',
        enabling author_instance.books.all() to fetch all related books.
    """
    name = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.name


class Book(models.Model):
    """
    A book written by an Author.

    Fields:
        title: Book title.
        publication_year: Year the book was published (validated in serializer).
        author: FK to Author establishing a 1-to-many (Author -> Books).
               related_name='books' lets us access an author's books as
               author.books.all() and also powers the nested serializer.
    """
    title = models.CharField(max_length=255)
    publication_year = models.PositiveIntegerField()
    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE,
        related_name='books'
    )

    def __str__(self) -> str:
        return f"{self.title} ({self.publication_year})"