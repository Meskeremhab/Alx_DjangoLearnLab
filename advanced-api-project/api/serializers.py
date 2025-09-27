from datetime import date
from rest_framework import serializers
from .models import Author, Book


class BookSerializer(serializers.ModelSerializer):
    """
    Serializes all fields of Book.

    Custom validation:
        publication_year must not be in the future relative to today's year.
    """
    class Meta:
        model = Book
        fields = ["id", "title", "publication_year", "author"]

    def validate_publication_year(self, value: int) -> int:
        current_year = date.today().year
        if value > current_year:
            raise serializers.ValidationError(
                f"publication_year cannot be in the future (>{current_year})."
            )
        return value


class AuthorSerializer(serializers.ModelSerializer):
    """
    Serializes Author with a nested, read-only list of related Books.

    Relationship handling:
        The Book model defines related_name='books', so we can include
        books = BookSerializer(many=True) to serialize the 1-to-many relationship.
        This lets clients see an author's books in-line without separate calls.
    """
    books = BookSerializer(many=True, read_only=True)

    class Meta:
        model = Author
        fields = ["id", "name", "books"]
