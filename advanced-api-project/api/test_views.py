
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Author, Book

class BookAPITestCase(APITestCase):
    """
    Test suite for the BookListCreate (List/Create) and 
    BookDetailUpdateDelete (Retrieve/Update/Delete) endpoints.
    """
    
    def setUp(self):
        """
        Set up necessary objects for testing, including users and initial data.
        """
        # 1. Create users for authentication tests
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.unauthenticated_client = self.client # Default client is unauthenticated
        
        # 2. Create initial data
        self.author1 = Author.objects.create(name='Jane Austen')
        self.author2 = Author.objects.create(name='George Orwell')
        
        self.book1 = Book.objects.create(
            title='Pride and Prejudice', 
            publication_year=1813, 
            author=self.author1
        )
        self.book2 = Book.objects.create(
            title='Animal Farm', 
            publication_year=1945, 
            author=self.author2
        )
        self.book3 = Book.objects.create(
            title='1984', 
            publication_year=1949, 
            author=self.author2
        )
        
        # 3. Define URLs
        self.list_url = reverse('book-list-create')
        self.detail_url = reverse('book-detail-update-delete', kwargs={'pk': self.book1.pk})
        
        # 4. Define valid payload for POST/PUT requests
        self.valid_payload = {
            'title': 'New Test Book',
            'publication_year': 2024,
            'author': self.author1.pk # Must reference a valid Author ID
        }
        
# --- 1. CRUD Operation Tests ---

    def test_list_books(self):
        """
        Test that listing all books returns the correct data and status code.
        """
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 3)
        self.assertEqual(response.data['results'][0]['title'], 'Pride and Prejudice')

    def test_retrieve_book(self):
        """
        Test retrieving a single book by ID.
        """
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Pride and Prejudice')
        self.assertEqual(response.data['publication_year'], 1813)

    def test_create_book_authenticated(self):
        """
        Test that an authenticated user can successfully create a new book.
        """
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.list_url, self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 4) # Check database count increased
        self.assertEqual(response.data['title'], 'New Test Book')

    def test_update_book_authenticated(self):
        """
        Test that an authenticated user can successfully update a book.
        """
        self.client.force_authenticate(user=self.user)
        updated_payload = {'title': 'Updated Title', 'publication_year': 2000, 'author': self.author2.pk}
        response = self.client.put(self.detail_url, updated_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, 'Updated Title')

    def test_delete_book_authenticated(self):
        """
        Test that an authenticated user can successfully delete a book.
        """
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 2) # Check database count decreased
        self.assertFalse(Book.objects.filter(pk=self.book1.pk).exists())

# --- 2. Permission/Authentication Tests ---

    def test_create_book_unauthenticated_denied(self):
        """
        Test that an unauthenticated user is denied from creating a book (POST).
        """
        response = self.unauthenticated_client.post(self.list_url, self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Book.objects.count(), 3) # Count should not change

    def test_update_book_unauthenticated_denied(self):
        """
        Test that an unauthenticated user is denied from updating a book (PUT).
        """
        updated_payload = {'title': 'Attempted Update', 'publication_year': 2000, 'author': self.author1.pk}
        response = self.unauthenticated_client.put(self.detail_url, updated_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.book1.refresh_from_db()
        self.assertNotEqual(self.book1.title, 'Attempted Update')

# --- 3. Filtering, Searching, and Ordering Tests ---

    def test_filter_by_publication_year(self):
        """
        Test filtering by exact publication_year.
        """
        # We have books from 1813, 1945, 1949
        response = self.client.get(f'{self.list_url}?publication_year=1945')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['title'], 'Animal Farm')

    def test_search_by_title(self):
        """
        Test searching for a term in the title field.
        """
        response = self.client.get(f'{self.list_url}?search=Prejudice')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['title'], 'Pride and Prejudice')
        
    def test_search_by_author_name(self):
        """
        Test searching for a term in the linked author name field.
        """
        response = self.client.get(f'{self.list_url}?search=Orwell')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)
        
    def test_ordering_ascending(self):
        """
        Test ordering results by publication_year ascending.
        Expected order: 1813, 1945, 1949
        """
        response = self.client.get(f'{self.list_url}?ordering=publication_year')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.data['results']
        self.assertEqual(results[0]['publication_year'], 1813)
        self.assertEqual(results[1]['publication_year'], 1945)
        self.assertEqual(results[2]['publication_year'], 1949)

    def test_ordering_descending(self):
        """
        Test ordering results by publication_year descending.
        Expected order: 1949, 1945, 1813
        """
        response = self.client.get(f'{self.list_url}?ordering=-publication_year')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.data['results']
        self.assertEqual(results[0]['publication_year'], 1949)
        self.assertEqual(results[2]['publication_year'], 1813)