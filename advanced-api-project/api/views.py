# api/views.py
from rest_framework import generics, parsers, serializers
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated  
from .models import Book
from .serializers import BookSerializer

from rest_framework.filters import SearchFilter, OrderingFilter              
from django_filters.rest_framework import DjangoFilterBackend                

from .filters import BookFilter  
from rest_framework import generics, parsers, serializers
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.filters import SearchFilter, OrderingFilter          # <-- required
from django_filters import rest_framework as filters                     # <-- required (exact substring)


class BookListView(generics.ListAPIView):
    """
    List books with filtering, searching, and ordering.

    Examples:
      /books/?author=1
      /books/?publication_year=1993
      /books/?search=parable
      /books/?ordering=-publication_year
    """
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Book.objects.select_related("author").all()

    # DRF backends
    filter_backends = [filters.DjangoFilterBackend, SearchFilter, OrderingFilter]

    # Filtering (exact fields)
    filterset_fields = ["title", "author", "publication_year"]

    # Search (text)
    search_fields = ["title", "author__name"]

    # Ordering
    ordering_fields = ["id", "title", "publication_year", "author"]
    ordering = ["publication_year"]  # default


class BookDetailView(generics.RetrieveAPIView):
    queryset = Book.objects.select_related("author")
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class BookCreateView(generics.CreateAPIView):
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [parsers.JSONParser, parsers.FormParser, parsers.MultiPartParser]

    def perform_create(self, serializer):
        data = serializer.validated_data
        if Book.objects.filter(
            title=data["title"],
            publication_year=data["publication_year"],
            author=data["author"],
        ).exists():
            raise serializers.ValidationError(
                {"non_field_errors": ["This author already has a book with the same title and year."]}
            )
        serializer.save()


class BookUpdateView(generics.UpdateAPIView):
    queryset = Book.objects.select_related("author")
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [parsers.JSONParser, parsers.FormParser, parsers.MultiPartParser]

    def perform_update(self, serializer):
        instance = self.get_object()
        data = serializer.validated_data
        if Book.objects.exclude(pk=instance.pk).filter(
            title=data.get("title", instance.title),
            publication_year=data.get("publication_year", instance.publication_year),
            author=data.get("author", instance.author),
        ).exists():
            raise serializers.ValidationError(
                {"non_field_errors": ["Another book with the same title and year for this author already exists."]}
            )
        serializer.save()


class BookDeleteView(generics.DestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]