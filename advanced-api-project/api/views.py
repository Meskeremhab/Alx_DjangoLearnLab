# api/views.py
from rest_framework import generics, parsers, serializers
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated  
from .models import Book
from .serializers import BookSerializer

from rest_framework.filters import SearchFilter, OrderingFilter              
from django_filters.rest_framework import DjangoFilterBackend                

from .filters import BookFilter  

class BookListView(generics.ListAPIView):
    """
    Read-only list with:
      - Filtering (title, author, publication_year + year_min/year_max)
      - Searching (title, author name)
      - Ordering (id, title, publication_year, author)
    Examples:
      /books/?author=1
      /books/?year_min=1980&year_max=2000
      /books/?search=parab
      /books/?ordering=-publication_year
    """
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Book.objects.select_related("author").all()

    # DRF backends
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = BookFilter
    search_fields = ["title", "author__name"]
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