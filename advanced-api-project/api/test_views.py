"""
Comprehensive unit tests for Django REST Framework APIs

This module contains unit tests for the Book and Author API endpoints,
testing CRUD operations, filtering, searching, ordering, and authentication.
"""

from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from api.models import Book, Author
from api.serializers import BookSerializer, AuthorSerializer
import json


class BookAPITestCase(APITestCase):
    """Test cases for Book API endpoints"""
    
    def setUp(self):
        """Set up test data and client"""
        # Create test users
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.admin_user = User.objects.create_user(
            username='admin',
            password='adminpass123',
            is_staff=True
        )
        
        # Create test authors
        self.author1 = Author.objects.create(name='J.K. Rowling')
        self.author2 = Author.objects.create(name='George Orwell')
        
        # Create test books
        self.book1 = Book.objects.create(
            title='Harry Potter',
            publication_year=1997,
            author=self.author1
        )
        self.book2 = Book.objects.create(
            title='1984',
            publication_year=1949,
            author=self.author2
        )
        
        # Create API client
        self.client = APIClient()
    
    def test_list_books_authenticated(self):
        """Test listing books with authentication"""
        self.client.login(username='testuser', password='testpass123')
        url = reverse('book-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        
        # Check if all required fields are present
        book_data = response.data[0]
        self.assertIn('id', book_data)
        self.assertIn('title', book_data)
        self.assertIn('publication_year', book_data)
        self.assertIn('author', book_data)
    
    def test_list_books_unauthenticated(self):
        """Test listing books without authentication (should work due to IsAuthenticatedOrReadOnly)"""
        url = reverse('book-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
    
    def test_retrieve_book_detail(self):
        """Test retrieving a specific book"""
        url = reverse('book-detail', kwargs={'pk': self.book1.pk})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Harry Potter')
        self.assertEqual(response.data['publication_year'], 1997)
        self.assertEqual(response.data['author'], self.author1.id)
    
    def test_retrieve_nonexistent_book(self):
        """Test retrieving a book that doesn't exist"""
        url = reverse('book-detail', kwargs={'pk': 999})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_create_book_authenticated(self):
        """Test creating a book with authentication"""
        self.client.login(username='testuser', password='testpass123')
        url = reverse('book-create')
        
        data = {
            'title': 'The Great Gatsby',
            'publication_year': 1925,
            'author': self.author1.id
        }
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 3)
        
        # Verify the book was created correctly
        book = Book.objects.get(title='The Great Gatsby')
        self.assertEqual(book.publication_year, 1925)
        self.assertEqual(book.author, self.author1)
    
    def test_create_book_unauthenticated(self):
        """Test creating a book without authentication (should fail)"""
        url = reverse('book-create')
        
        data = {
            'title': 'The Great Gatsby',
            'publication_year': 1925,
            'author': self.author1.id
        }
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Book.objects.count(), 2)
    
    def test_create_book_invalid_data(self):
        """Test creating a book with invalid data"""
        self.client.login(username='testuser', password='testpass123')
        url = reverse('book-create')
        
        # Test invalid publication year (too old)
        data = {
            'title': 'Ancient Book',
            'publication_year': 500,
            'author': self.author1.id
        }
        
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        # Test invalid publication year (too new)
        data = {
            'title': 'Future Book',
            'publication_year': 2030,
            'author': self.author1.id
        }
        
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_update_book_authenticated(self):
        """Test updating a book with authentication"""
        self.client.login(username='testuser', password='testpass123')
        url = reverse('book-update', kwargs={'pk': self.book1.pk})
        
        data = {
            'title': 'Harry Potter and the Philosopher\'s Stone',
            'publication_year': 1997,
            'author': self.author1.id
        }
        
        response = self.client.put(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verify the book was updated
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, 'Harry Potter and the Philosopher\'s Stone')
    
    def test_update_book_unauthenticated(self):
        """Test updating a book without authentication (should fail)"""
        url = reverse('book-update', kwargs={'pk': self.book1.pk})
        
        data = {
            'title': 'Updated Title',
            'publication_year': 1997,
            'author': self.author1.id
        }
        
        response = self.client.put(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_delete_book_authenticated(self):
        """Test deleting a book with authentication"""
        self.client.login(username='testuser', password='testpass123')
        url = reverse('book-delete', kwargs={'pk': self.book1.pk})
        
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 1)
        self.assertFalse(Book.objects.filter(pk=self.book1.pk).exists())
    
    def test_delete_book_unauthenticated(self):
        """Test deleting a book without authentication (should fail)"""
        url = reverse('book-delete', kwargs={'pk': self.book1.pk})
        
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Book.objects.count(), 2)
    
    def test_delete_nonexistent_book(self):
        """Test deleting a book that doesn't exist"""
        self.client.login(username='testuser', password='testpass123')
        url = reverse('book-delete', kwargs={'pk': 999})
        
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class BookFilteringTestCase(APITestCase):
    """Test cases for Book filtering, searching, and ordering functionality"""
    
    def setUp(self):
        """Set up test data for filtering tests"""
        # Create test authors
        self.author1 = Author.objects.create(name='J.K. Rowling')
        self.author2 = Author.objects.create(name='George Orwell')
        self.author3 = Author.objects.create(name='Jane Austen')
        
        # Create test books with different years and authors
        self.book1 = Book.objects.create(
            title='Harry Potter',
            publication_year=1997,
            author=self.author1
        )
        self.book2 = Book.objects.create(
            title='1984',
            publication_year=1949,
            author=self.author2
        )
        self.book3 = Book.objects.create(
            title='Pride and Prejudice',
            publication_year=1813,
            author=self.author3
        )
        self.book4 = Book.objects.create(
            title='Animal Farm',
            publication_year=1945,
            author=self.author2
        )
    
    def test_filter_by_author(self):
        """Test filtering books by author"""
        url = reverse('book-list')
        response = self.client.get(url, {'author': self.author2.id})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        
        # Check that all returned books belong to the specified author
        for book in response.data:
            self.assertEqual(book['author'], self.author2.id)
    
    def test_filter_by_publication_year(self):
        """Test filtering books by publication year"""
        url = reverse('book-list')
        response = self.client.get(url, {'publication_year': 1949})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], '1984')
    
    def test_filter_by_multiple_fields(self):
        """Test filtering books by multiple fields"""
        url = reverse('book-list')
        response = self.client.get(url, {
            'author': self.author2.id,
            'publication_year': 1945
        })
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Animal Farm')
    
    def test_search_by_title(self):
        """Test searching books by title"""
        url = reverse('book-list')
        response = self.client.get(url, {'search': 'Harry'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Harry Potter')
    
    def test_search_by_author_name(self):
        """Test searching books by author name"""
        url = reverse('book-list')
        response = self.client.get(url, {'search': 'Orwell'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        
        # Check that both Orwell books are returned
        titles = [book['title'] for book in response.data]
        self.assertIn('1984', titles)
        self.assertIn('Animal Farm', titles)
    
    def test_search_by_publication_year(self):
        """Test searching books by publication year"""
        url = reverse('book-list')
        response = self.client.get(url, {'search': '1949'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], '1984')
    
    def test_ordering_by_title_ascending(self):
        """Test ordering books by title in ascending order"""
        url = reverse('book-list')
        response = self.client.get(url, {'ordering': 'title'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)
        
        # Check that books are ordered by title
        titles = [book['title'] for book in response.data]
        self.assertEqual(titles, sorted(titles))
    
    def test_ordering_by_title_descending(self):
        """Test ordering books by title in descending order"""
        url = reverse('book-list')
        response = self.client.get(url, {'ordering': '-title'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)
        
        # Check that books are ordered by title in descending order
        titles = [book['title'] for book in response.data]
        self.assertEqual(titles, sorted(titles, reverse=True))
    
    def test_ordering_by_publication_year(self):
        """Test ordering books by publication year"""
        url = reverse('book-list')
        response = self.client.get(url, {'ordering': 'publication_year'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)
        
        # Check that books are ordered by publication year
        years = [book['publication_year'] for book in response.data]
        self.assertEqual(years, sorted(years))
    
    def test_ordering_by_multiple_fields(self):
        """Test ordering books by multiple fields"""
        url = reverse('book-list')
        response = self.client.get(url, {'ordering': 'publication_year,title'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)
        
        # Check that books are ordered by publication year first, then title
        books = response.data
        for i in range(len(books) - 1):
            current_book = books[i]
            next_book = books[i + 1]
            
            if current_book['publication_year'] == next_book['publication_year']:
                self.assertLessEqual(current_book['title'], next_book['title'])
            else:
                self.assertLessEqual(current_book['publication_year'], next_book['publication_year'])
    
    def test_combined_filtering_searching_ordering(self):
        """Test combining filtering, searching, and ordering"""
        url = reverse('book-list')
        response = self.client.get(url, {
            'author': self.author2.id,
            'search': '19',
            'ordering': 'publication_year'
        })
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        
        # Check that results are filtered by author and contain '19' in search
        for book in response.data:
            self.assertEqual(book['author'], self.author2.id)
            self.assertTrue('19' in str(book['publication_year']) or '19' in book['title'])
        
        # Check that results are ordered by publication year
        years = [book['publication_year'] for book in response.data]
        self.assertEqual(years, sorted(years))


class AuthorAPITestCase(APITestCase):
    """Test cases for Author API endpoints"""
    
    def setUp(self):
        """Set up test data for author tests"""
        self.author1 = Author.objects.create(name='J.K. Rowling')
        self.author2 = Author.objects.create(name='George Orwell')
        
        # Create books for the authors
        self.book1 = Book.objects.create(
            title='Harry Potter',
            publication_year=1997,
            author=self.author1
        )
        self.book2 = Book.objects.create(
            title='1984',
            publication_year=1949,
            author=self.author2
        )
    
    def test_list_authors(self):
        """Test listing all authors"""
        url = reverse('author-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        
        # Check that author data includes books
        for author in response.data:
            self.assertIn('id', author)
            self.assertIn('name', author)
            self.assertIn('books', author)
    
    def test_retrieve_author_detail(self):
        """Test retrieving a specific author"""
        url = reverse('author-detail', kwargs={'pk': self.author1.pk})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'J.K. Rowling')
        self.assertEqual(len(response.data['books']), 1)
        self.assertEqual(response.data['books'][0], 'Harry Potter')
    
    def test_create_author(self):
        """Test creating a new author"""
        url = reverse('author-list')
        data = {'name': 'Jane Austen'}
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Author.objects.count(), 3)
        
        # Verify the author was created
        author = Author.objects.get(name='Jane Austen')
        self.assertEqual(author.name, 'Jane Austen')
    
    def test_update_author(self):
        """Test updating an author"""
        url = reverse('author-detail', kwargs={'pk': self.author1.pk})
        data = {'name': 'Joanne Rowling'}
        
        response = self.client.put(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verify the author was updated
        self.author1.refresh_from_db()
        self.assertEqual(self.author1.name, 'Joanne Rowling')
    
    def test_delete_author(self):
        """Test deleting an author"""
        url = reverse('author-detail', kwargs={'pk': self.author1.pk})
        
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Author.objects.count(), 1)
        self.assertFalse(Author.objects.filter(pk=self.author1.pk).exists())
    
    def test_filter_authors_by_name(self):
        """Test filtering authors by name"""
        url = reverse('author-list')
        response = self.client.get(url, {'name': 'J.K. Rowling'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'J.K. Rowling')
    
    def test_search_authors_by_name(self):
        """Test searching authors by name"""
        url = reverse('author-list')
        response = self.client.get(url, {'search': 'Rowling'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'J.K. Rowling')
    
    def test_ordering_authors_by_name(self):
        """Test ordering authors by name"""
        url = reverse('author-list')
        response = self.client.get(url, {'ordering': 'name'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        
        # Check that authors are ordered by name
        names = [author['name'] for author in response.data]
        self.assertEqual(names, sorted(names))


class SerializerValidationTestCase(TestCase):
    """Test cases for serializer validation"""
    
    def setUp(self):
        """Set up test data for serializer tests"""
        self.author = Author.objects.create(name='Test Author')
    
    def test_book_serializer_valid_data(self):
        """Test BookSerializer with valid data"""
        data = {
            'title': 'Test Book',
            'publication_year': 2020,
            'author': self.author.id
        }
        
        serializer = BookSerializer(data=data)
        self.assertTrue(serializer.is_valid())
    
    def test_book_serializer_invalid_year_too_old(self):
        """Test BookSerializer with publication year too old"""
        data = {
            'title': 'Test Book',
            'publication_year': 500,
            'author': self.author.id
        }
        
        serializer = BookSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('Publication year must be between 1000 and 2024', str(serializer.errors))
    
    def test_book_serializer_invalid_year_too_new(self):
        """Test BookSerializer with publication year too new"""
        data = {
            'title': 'Test Book',
            'publication_year': 2030,
            'author': self.author.id
        }
        
        serializer = BookSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('Publication year must be between 1000 and 2024', str(serializer.errors))
    
    def test_author_serializer_valid_data(self):
        """Test AuthorSerializer with valid data"""
        data = {'name': 'Test Author'}
        
        serializer = AuthorSerializer(data=data)
        self.assertTrue(serializer.is_valid())
    
    def test_author_serializer_with_books(self):
        """Test AuthorSerializer serializing author with books"""
        book = Book.objects.create(
            title='Test Book',
            publication_year=2020,
            author=self.author
        )
        
        serializer = AuthorSerializer(self.author)
        data = serializer.data
        
        self.assertEqual(data['name'], 'Test Author')
        self.assertEqual(len(data['books']), 1)
        self.assertEqual(data['books'][0], 'Test Book')


class ModelTestCase(TestCase):
    """Test cases for model functionality"""
    
    def test_author_model_creation(self):
        """Test Author model creation"""
        author = Author.objects.create(name='Test Author')
        
        self.assertEqual(author.name, 'Test Author')
        self.assertIsNotNone(author.id)
    
    def test_book_model_creation(self):
        """Test Book model creation"""
        author = Author.objects.create(name='Test Author')
        book = Book.objects.create(
            title='Test Book',
            publication_year=2020,
            author=author
        )
        
        self.assertEqual(book.title, 'Test Book')
        self.assertEqual(book.publication_year, 2020)
        self.assertEqual(book.author, author)
        self.assertIsNotNone(book.id)
    
    def test_book_str_representation(self):
        """Test Book model string representation"""
        author = Author.objects.create(name='Test Author')
        book = Book.objects.create(
            title='Test Book',
            publication_year=2020,
            author=author
        )
        
        self.assertEqual(str(book), 'Test Book')
    
    def test_author_book_relationship(self):
        """Test the relationship between Author and Book models"""
        author = Author.objects.create(name='Test Author')
        book1 = Book.objects.create(
            title='Book 1',
            publication_year=2020,
            author=author
        )
        book2 = Book.objects.create(
            title='Book 2',
            publication_year=2021,
            author=author
        )
        
        # Test forward relationship
        self.assertEqual(book1.author, author)
        self.assertEqual(book2.author, author)
        
        # Test reverse relationship
        author_books = author.book_set.all()
        self.assertEqual(len(author_books), 2)
        self.assertIn(book1, author_books)
        self.assertIn(book2, author_books)
