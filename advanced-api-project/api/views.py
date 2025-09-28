# api/views.py
from rest_framework import generics, parsers, serializers
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated  # <-- add this line
from .models import Book
from .serializers import BookSerializer


class BookQueryMixin:
    def get_queryset(self):
        qs = Book.objects.select_related("author").all()
        author_id = self.request.query_params.get("author")
        year_min = self.request.query_params.get("year_min")
        year_max = self.request.query_params.get("year_max")
        ordering = self.request.query_params.get("ordering")

        if author_id:
            qs = qs.filter(author_id=author_id)
        if year_min:
            qs = qs.filter(publication_year__gte=year_min)
        if year_max:
            qs = qs.filter(publication_year__lte=year_max)
        if ordering in ("publication_year", "-publication_year"):
            qs = qs.order_by(ordering)
        return qs


class BookListView(BookQueryMixin, generics.ListAPIView):
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]  # public read


class BookDetailView(generics.RetrieveAPIView):
    queryset = Book.objects.select_related("author")
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]  # public read


class BookCreateView(generics.CreateAPIView):
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]  # auth required
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
    permission_classes = [IsAuthenticated]  # auth required
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
    permission_classes = [IsAuthenticated]  # auth required
