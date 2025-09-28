import django_filters
from .models import Book

class BookFilter(django_filters.FilterSet):
    # Range helpers
    year_min = django_filters.NumberFilter(field_name="publication_year", lookup_expr="gte")
    year_max = django_filters.NumberFilter(field_name="publication_year", lookup_expr="lte")

    class Meta:
        model = Book
        # exact-match filters (DRF will combine with the custom ones above)
        fields = ["title", "author", "publication_year"]
