from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth.models import User
from api.models import Book

class BookAPITestCase(APITestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.client = APIClient()
        self.client.login(username="testuser", password="testpass")

        # Create some test data
        self.book1 = Book.objects.create(title="Book 1", author="Author A", published_year=2020)
        self.book2 = Book.objects.create(title="Book 2", author="Author B", published_year=2021)

        self.valid_data = {"title": "New Book", "author": "Author C", "published_year": 2022}
        self.invalid_data = {"title": "", "author": "Author C", "published_year": 2022}

    def test_create_book(self):
        response = self.client.post('/api/books/', data=self.valid_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 3)
        self.assertEqual(response.data["title"], "New Book")

    def test_get_books(self):
        response = self.client.get('/api/books/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_update_book(self):
        response = self.client.put(f'/api/books/{self.book1.id}/', data={"title": "Updated Book", "author": "Author A", "published_year": 2020})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, "Updated Book")

    def test_delete_book(self):
        response = self.client.delete(f'/api/books/{self.book2.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 1)
