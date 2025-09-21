from rest_framework import serializers
from .models import Book

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        # EITHER list them explicitly:
        fields = ["id", "title", "author"]
        # OR use all fields:
        # fields = "__all__"
