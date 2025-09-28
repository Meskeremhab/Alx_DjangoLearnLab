# api/test_views.py
from datetime import date

from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from .models import Author, Book


class BookAPITests(TestCase):
    """
    Integration-style API tests for the Book endpoints.

    Endpoints under test (from api/urls.py):
      - GET  /books/                       -> book-list
      - GET  /books/<pk>/                  -> book-detail
      - POST /books/create/                -> book-create        (auth required)
      - PUT  /books/update/<pk>/           -> book-update        (auth required)
      - DELETE /books/delete/<pk>/         -> book-delete        (auth required)

    Features under test:
      - CRUD: create, retrieve, update, delete
      - Permissions: public read, auth-only write
      - Filtering: ?title=, ?author=, ?publication_year=
      - Searching: ?search= across title and author__name
      - Ordering:  ?ordering=title / -publication_year / etc.
    """

    @classmethod
    def setUpTestData(cls):
        # Users
        User = get_user_model()
        cls.user = User.objects.create_user(username="tester", password="pass1234")

        # Authors + Books
        cls.author1 = Author.objects.create(name="Author One")
        cls.author2 = Author.objects.create(name="Author Two")

        cls.book1 = Book.objects.create(
            title="Alpha", publication_year=1990, author=cls.author1
        )
        cls.book2 = Book.objects.create(
            title="Beta", publication_year=2000, author=cls.author2
        )

        # URLs
        cls.list_url = reverse("book-list")
        cls.create_url = reverse("book-create")

    def setUp(self):
        self.client = APIClient()

    # ----------------------
    # READ (public allowed)
    # ----------------------
    def test_list_books_public(self):
        res = self.client.get(self.list_url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertTrue(isinstance(res.data, list))
        self.assertGreaterEqual(len(res.data), 2)

    def test_retrieve_book_public(self):
        url = reverse("book-detail", args=[self.book1.id])
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["id"], self.book1.id)
        self.assertEqual(res.data["title"], "Alpha")

    # ----------------------
    # CREATE (auth required)
    # ----------------------
    def test_create_book_requires_auth(self):
        payload = {"title": "Gamma", "publication_year": 2010, "author": self.author1.id}
        res = self.client.post(self.create_url, payload, format="json")
        # SessionAuth unauthenticated typically yields 403
        self.assertIn(res.status_code, (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN))
        self.assertFalse(Book.objects.filter(title="Gamma").exists())

    def test_create_book_authenticated_success(self):
        self.client.force_authenticate(user=self.user)
        payload = {"title": "Gamma", "publication_year": 2010, "author": self.author1.id}
        res = self.client.post(self.create_url, payload, format="json")
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Book.objects.filter(title="Gamma", author=self.author1).exists())

    def test_create_book_rejects_future_year(self):
        self.client.force_authenticate(user=self.user)
        future_year = date.today().year + 1
        payload = {"title": "Future Book", "publication_year": future_year, "author": self.author1.id}
        res = self.client.post(self.create_url, payload, format="json")
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("publication_year", res.data)

    def test_create_book_duplicate_rule(self):
        """Creating same (title, publication_year, author) should error (custom rule)."""
        self.client.force_authenticate(user=self.user)
        payload = {"title": "Alpha", "publication_year": 1990, "author": self.author1.id}
        res = self.client.post(self.create_url, payload, format="json")
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        # non_field_errors is what we raise in perform_create
        self.assertIn("non_field_errors", res.data)

    # ----------------------
    # UPDATE (auth required)
    # ----------------------
    def test_update_requires_auth(self):
        url = reverse("book-update", args=[self.book1.id])
        payload = {"title": "Alpha (Updated)", "publication_year": 1991, "author": self.author1.id}
        res = self.client.put(url, payload, format="json")
        self.assertIn(res.status_code, (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN))
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, "Alpha")

    def test_update_authenticated_success(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("book-update", args=[self.book1.id])
        payload = {"title": "Alpha (Updated)", "publication_year": 1991, "author": self.author1.id}
        res = self.client.put(url, payload, format="json")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, "Alpha (Updated)")
        self.assertEqual(self.book1.publication_year, 1991)

    # ----------------------
    # DELETE (auth required)
    # ----------------------
    def test_delete_requires_auth(self):
        url = reverse("book-delete", args=[self.book2.id])
        res = self.client.delete(url)
        self.assertIn(res.status_code, (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN))
        self.assertTrue(Book.objects.filter(pk=self.book2.id).exists())

    def test_delete_authenticated_success(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("book-delete", args=[self.book2.id])
        res = self.client.delete(url)
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Book.objects.filter(pk=self.book2.id).exists())

    # ----------------------
    # FILTERING / SEARCH / ORDER
    # ----------------------
    def test_filter_by_author(self):
        res = self.client.get(f"{self.list_url}?author={self.author1.id}")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        ids = [b["id"] for b in res.data]
        self.assertIn(self.book1.id, ids)
        self.assertNotIn(self.book2.id, ids)

    def test_filter_by_publication_year(self):
        res = self.client.get(f"{self.list_url}?publication_year=2000")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]["id"], self.book2.id)

    def test_search_by_title(self):
        res = self.client.get(f"{self.list_url}?search=alp")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        ids = [b["id"] for b in res.data]
        self.assertIn(self.book1.id, ids)

    def test_search_by_author_name(self):
        res = self.client.get(f"{self.list_url}?search=Author%20Two")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        ids = [b["id"] for b in res.data]
        self.assertIn(self.book2.id, ids)

    def test_ordering_desc_publication_year(self):
        res = self.client.get(f"{self.list_url}?ordering=-publication_year")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        # Expect book2 (2000) before book1 (1990)
        returned_ids = [b["id"] for b in res.data]
        self.assertEqual(returned_ids[:2], [self.book2.id, self.book1.id])
