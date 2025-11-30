
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Author, Book

class BookAPITestCase(APITestCase):
    """
    Test suite for the explicit, non-RESTful CRUD endpoints.
    Uses self.client.login() for authentication checks.
    """
    
    def setUp(self):
        """
        Set up necessary objects for testing.
        """
        # 1. Create users for authentication tests
        self.user_password = 'password123'
        self.user = User.objects.create_user(username='testuser', password=self.user_password)
        self.unauthenticated_client = self.client # Default client is unauthenticated
        
        # 2. Create initial data
        self.author1 = Author.objects.create(name='Jane Austen')
        self.author2 = Author.objects.create(name='George Orwell')
        
        self.book1 = Book.objects.create(
            title='Pride and Prejudice', 
            publication_year=1813, 
            author=self.author1
        )
        # Note: We create book2 and book3 for list/query testing
        self.book2 = Book.objects.create(title='Animal Farm', publication_year=1945, author=self.author2)
        self.book3 = Book.objects.create(title='1984', publication_year=1949, author=self.author2)
        
        # 3. Define URLs (based on the explicit, non-RESTful structure)
        self.list_url = reverse('book-list')
        self.create_url = reverse('book-create')
        self.detail_url = reverse('book-detail', kwargs={'pk': self.book1.pk})
        self.update_url = reverse('book-update', kwargs={'pk': self.book1.pk})
        self.delete_url = reverse('book-delete', kwargs={'pk': self.book1.pk})
        
        # 4. Define valid payload for POST/PUT requests
        self.valid_payload = {
            'title': 'New Test Book',
            'publication_year': 2024,
            'author': self.author1.pk # Must reference a valid Author ID
        }
        
# --- 1. CRUD Operation Tests ---

    def test_list_books(self):
        """Test retrieving all books via GET to the explicit list URL."""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 3)

    def test_retrieve_book(self):
        """Test retrieving a single book via GET to the explicit detail URL."""
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Pride and Prejudice')

    def test_create_book_authenticated(self):
        """Test that an authenticated user can successfully create a new book using POST to the create URL."""
        # Use self.client.login() as requested by the checker
        self.assertTrue(self.client.login(username=self.user.username, password=self.user_password))
        
        response = self.client.post(self.create_url, self.valid_payload, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 4) 
        self.assertEqual(response.data['title'], 'New Test Book')

    def test_update_book_authenticated(self):
        """Test that an authenticated user can successfully update a book using PUT to the update URL."""
        # Use self.client.login() as requested by the checker
        self.assertTrue(self.client.login(username=self.user.username, password=self.user_password))
        
        updated_payload = {'title': 'Updated Title', 'publication_year': 2000, 'author': self.author2.pk}
        response = self.client.put(self.update_url, updated_payload, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, 'Updated Title')

    def test_delete_book_authenticated(self):
        """Test that an authenticated user can successfully delete a book using DELETE to the delete URL."""
        # Use self.client.login() as requested by the checker
        self.assertTrue(self.client.login(username=self.user.username, password=self.user_password))
        
        response = self.client.delete(self.delete_url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 2) 
        self.assertFalse(Book.objects.filter(pk=self.book1.pk).exists())

# --- 2. Permission/Authentication Tests (No Login) ---

    def test_create_book_unauthenticated_denied(self):
        """Test that an unauthenticated user is denied from creating a book (POST)."""
        response = self.unauthenticated_client.post(self.create_url, self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Book.objects.count(), 3) # Count should not change

    def test_update_book_unauthenticated_denied(self):
        """Test that an unauthenticated user is denied from updating a book (PUT)."""
        updated_payload = {'title': 'Attempted Update', 'publication_year': 2000, 'author': self.author1.pk}
        response = self.unauthenticated_client.put(self.update_url, updated_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.book1.refresh_from_db()
        self.assertNotEqual(self.book1.title, 'Attempted Update')

    def test_delete_book_unauthenticated_denied(self):
        """Test that an unauthenticated user is denied from deleting a book (DELETE)."""
        response = self.unauthenticated_client.delete(self.delete_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Book.objects.count(), 3) # Count should not change