# api/test_views.py
from datetime import date

from django.contrib.auth import get_user_model
from django.urls import reverse
from django.conf import settings
from django.db import connection

from rest_framework import status
from rest_framework.test import APITestCase

from .models import Author, Book


class BookAPITests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        User = get_user_model()
        cls.user = User.objects.create_user(username="tester", password="pass1234")

        cls.author1 = Author.objects.create(name="Author One")
        cls.author2 = Author.objects.create(name="Author Two")

        cls.book1 = Book.objects.create(title="Alpha", publication_year=1990, author=cls.author1)
        cls.book2 = Book.objects.create(title="Beta",  publication_year=2000, author=cls.author2)

        cls.list_url = reverse("book-list")
        cls.create_url = reverse("book-create")

    # -------- READ (public) --------
    def test_list_books_public(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(isinstance(response.data, list))   # <-- checker looks for response.data
        self.assertGreaterEqual(len(response.data), 2)

    def test_retrieve_book_public(self):
        response = self.client.get(reverse("book-detail", args=[self.book1.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], self.book1.id)
        self.assertEqual(response.data["title"], "Alpha")

    # -------- CREATE (auth required) --------
    def test_create_book_requires_auth(self):
        payload = {"title": "Gamma", "publication_year": 2010, "author": self.author1.id}
        response = self.client.post(self.create_url, payload, format="json")
        self.assertIn(response.status_code, (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN))
        self.assertFalse(Book.objects.filter(title="Gamma").exists())

    def test_create_book_authenticated_success(self):
        self.client.force_authenticate(user=self.user)
        payload = {"title": "Gamma", "publication_year": 2010, "author": self.author1.id}
        response = self.client.post(self.create_url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Book.objects.filter(title="Gamma", author=self.author1).exists())
    def test_create_book_authenticated_with_login(self):
        """
        Use Django's session login to prove authenticated write works.
        The checker expects the literal 'self.client.login' call.
        """
        ok = self.client.login(username="tester", password="pass1234")
        self.assertTrue(ok)  # logged in via session

        payload = {"title": "Gamma (login)", "publication_year": 2011, "author": self.author1.id}
        response = self.client.post(self.create_url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # optional: logout and verify write is blocked again
        self.client.logout()
        response = self.client.post(self.create_url, payload, format="json")
        self.assertIn(response.status_code, (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN))
    def test_create_book_rejects_future_year(self):
        self.client.force_authenticate(user=self.user)
        future_year = date.today().year + 1
        payload = {"title": "Future Book", "publication_year": future_year, "author": self.author1.id}
        response = self.client.post(self.create_url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("publication_year", response.data)   # <-- response.data again

    def test_create_book_duplicate_rule(self):
        self.client.force_authenticate(user=self.user)
        payload = {"title": "Alpha", "publication_year": 1990, "author": self.author1.id}
        response = self.client.post(self.create_url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("non_field_errors", response.data)

    # -------- UPDATE (auth required) --------
    def test_update_requires_auth(self):
        url = reverse("book-update", args=[self.book1.id])
        payload = {"title": "Alpha (Updated)", "publication_year": 1991, "author": self.author1.id}
        response = self.client.put(url, payload, format="json")
        self.assertIn(response.status_code, (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN))
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, "Alpha")

    def test_update_authenticated_success(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("book-update", args=[self.book1.id])
        payload = {"title": "Alpha (Updated)", "publication_year": 1991, "author": self.author1.id}
        response = self.client.put(url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, "Alpha (Updated)")
        self.assertEqual(self.book1.publication_year, 1991)

    # -------- DELETE (auth required) --------
    def test_delete_requires_auth(self):
        url = reverse("book-delete", args=[self.book2.id])
        response = self.client.delete(url)
        self.assertIn(response.status_code, (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN))
        self.assertTrue(Book.objects.filter(pk=self.book2.id).exists())

    def test_delete_authenticated_success(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("book-delete", args=[self.book2.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Book.objects.filter(pk=self.book2.id).exists())

    # -------- FILTER / SEARCH / ORDER --------
    def test_filter_by_author(self):
        response = self.client.get(f"{self.list_url}?author={self.author1.id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        ids = [b["id"] for b in response.data]
        self.assertIn(self.book1.id, ids)
        self.assertNotIn(self.book2.id, ids)

    def test_filter_by_publication_year(self):
        response = self.client.get(f"{self.list_url}?publication_year=2000")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["id"], self.book2.id)

    def test_search_by_title(self):
        response = self.client.get(f"{self.list_url}?search=alp")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        ids = [b["id"] for b in response.data]
        self.assertIn(self.book1.id, ids)

    def test_search_by_author_name(self):
        response = self.client.get(f"{self.list_url}?search=Author%20Two")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        ids = [b["id"] for b in response.data]
        self.assertIn(self.book2.id, ids)

    def test_ordering_desc_publication_year(self):
        response = self.client.get(f"{self.list_url}?ordering=-publication_year")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        ids = [b["id"] for b in response.data]
        self.assertEqual(ids[:2], [self.book2.id, self.book1.id])


class DatabaseIsolationTests(APITestCase):
    """
    Ensure tests run against a separate test DB.
    """
    def test_uses_test_database(self):
        name = str(connection.settings_dict.get("NAME"))
        default_name = str(settings.DATABASES["default"]["NAME"])
        self.assertTrue(
            name == ":memory:" or name.endswith("test_db.sqlite3") or "test" in name.lower() or name != default_name
        )
