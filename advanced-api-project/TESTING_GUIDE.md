# Django REST Framework API Testing Guide

## Overview

This document provides comprehensive guidelines for testing Django REST Framework APIs, including the testing approach, test cases, and how to run and interpret test results.

## Testing Strategy

### Test Framework

- **Framework**: Django's built-in test framework (based on Python's unittest module)
- **Test Database**: Separate test database created automatically for each test run
- **Authentication**: Token-based authentication for API endpoints
- **Test Client**: Django REST Framework's APIClient for API testing

### Test Categories

#### 1. CRUD Operations Testing

- **Create**: Test book/author creation with valid and invalid data
- **Read**: Test listing and retrieving individual resources
- **Update**: Test updating existing resources
- **Delete**: Test deleting resources

#### 2. Authentication & Permissions Testing

- **Authenticated Requests**: Test endpoints requiring authentication
- **Unauthenticated Requests**: Test endpoints that should fail without authentication
- **Permission Levels**: Test different permission levels (IsAuthenticated, IsAuthenticatedOrReadOnly)

#### 3. Filtering, Searching & Ordering Testing

- **Filtering**: Test filtering by specific fields (author, publication_year)
- **Searching**: Test search functionality across multiple fields
- **Ordering**: Test ascending/descending ordering by different fields
- **Combined Operations**: Test filtering + searching + ordering together

#### 4. Serializer Validation Testing

- **Valid Data**: Test serializers with valid input data
- **Invalid Data**: Test serializers with invalid input data
- **Custom Validation**: Test custom validation rules (e.g., publication year range)

#### 5. Model Testing

- **Model Creation**: Test model instantiation and field validation
- **Relationships**: Test foreign key relationships between models
- **String Representation**: Test model `__str__` methods

## Test Structure

### Test Classes

1. **BookAPITestCase**: Tests for Book API endpoints

   - CRUD operations
   - Authentication requirements
   - Data validation

2. **BookFilteringTestCase**: Tests for Book filtering, searching, and ordering

   - Filter by author and publication year
   - Search by title, author name, and publication year
   - Order by title and publication year

3. **AuthorAPITestCase**: Tests for Author API endpoints

   - CRUD operations
   - Author-book relationships

4. **SerializerValidationTestCase**: Tests for serializer validation

   - Book serializer validation
   - Author serializer validation

5. **ModelTestCase**: Tests for model functionality
   - Model creation and relationships
   - String representations

### Authentication Setup

The tests use Token authentication instead of session-based authentication:

```python
# Create test users
self.user = User.objects.create_user(
    username='testuser',
    password='testpass123'
)

# Create authentication tokens
self.user_token, created = Token.objects.get_or_create(user=self.user)

# Use token authentication in requests
self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_token.key)
```

### Test Data Setup

Each test class includes a `setUp()` method that:

- Creates test users and authentication tokens
- Creates test authors and books
- Sets up the API client

## Running Tests

### Run All Tests

```bash
python manage.py test api
```

### Run Specific Test Class

```bash
python manage.py test api.test_views.BookAPITestCase
```

### Run Specific Test Method

```bash
python manage.py test api.test_views.BookAPITestCase.test_create_book_authenticated
```

### Run with Verbose Output

```bash
python manage.py test api -v 2
```

## Test Configuration

### Settings Configuration

The following settings are configured for testing:

```python
# settings.py
INSTALLED_APPS = [
    # ... other apps
    'rest_framework',
    'rest_framework.authtoken',
    'django_filters',
    'api'
]

REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ],
}
```

### Database Configuration

- **Test Database**: Automatically created in memory for each test run
- **Migrations**: Applied automatically before running tests
- **Data Isolation**: Each test runs in isolation with fresh data

## Test Cases Details

### Book API Tests

#### Authentication Tests

- `test_list_books_authenticated()`: Test listing books with authentication
- `test_list_books_unauthenticated()`: Test listing books without authentication (should work due to IsAuthenticatedOrReadOnly)
- `test_create_book_authenticated()`: Test creating books with authentication
- `test_create_book_unauthenticated()`: Test creating books without authentication (should fail)

#### CRUD Tests

- `test_retrieve_book_detail()`: Test retrieving a specific book
- `test_retrieve_nonexistent_book()`: Test retrieving a non-existent book
- `test_update_book_authenticated()`: Test updating books with authentication
- `test_delete_book_authenticated()`: Test deleting books with authentication

#### Validation Tests

- `test_create_book_invalid_data()`: Test creating books with invalid publication years

### Filtering Tests

#### Filter Tests

- `test_filter_by_author()`: Filter books by author
- `test_filter_by_publication_year()`: Filter books by publication year
- `test_filter_by_multiple_fields()`: Filter books by multiple fields

#### Search Tests

- `test_search_by_title()`: Search books by title
- `test_search_by_author_name()`: Search books by author name
- `test_search_by_publication_year()`: Search books by publication year

#### Ordering Tests

- `test_ordering_by_title_ascending()`: Order books by title (ascending)
- `test_ordering_by_title_descending()`: Order books by title (descending)
- `test_ordering_by_publication_year()`: Order books by publication year
- `test_ordering_by_multiple_fields()`: Order books by multiple fields

#### Combined Tests

- `test_combined_filtering_searching_ordering()`: Test filtering + searching + ordering together

### Author API Tests

#### CRUD Tests

- `test_list_authors()`: Test listing all authors
- `test_retrieve_author_detail()`: Test retrieving a specific author
- `test_create_author()`: Test creating a new author
- `test_update_author()`: Test updating an author
- `test_delete_author()`: Test deleting an author

#### Filtering Tests

- `test_filter_authors_by_name()`: Filter authors by name
- `test_search_authors_by_name()`: Search authors by name
- `test_ordering_authors_by_name()`: Order authors by name

### Serializer Tests

#### Book Serializer Tests

- `test_book_serializer_valid_data()`: Test with valid data
- `test_book_serializer_invalid_year_too_old()`: Test with publication year too old
- `test_book_serializer_invalid_year_too_new()`: Test with publication year too new

#### Author Serializer Tests

- `test_author_serializer_valid_data()`: Test with valid data
- `test_author_serializer_with_books()`: Test serializing author with books

### Model Tests

#### Model Creation Tests

- `test_author_model_creation()`: Test Author model creation
- `test_book_model_creation()`: Test Book model creation
- `test_book_str_representation()`: Test Book model string representation

#### Relationship Tests

- `test_author_book_relationship()`: Test Author-Book relationship

## Interpreting Test Results

### Success Indicators

- All tests pass with "OK" status
- No errors or failures reported
- Test database created and destroyed successfully

### Common Issues and Solutions

#### Authentication Errors

- **Issue**: `AttributeError: type object 'Token' has no attribute 'objects'`
- **Solution**: Ensure `rest_framework.authtoken` is in INSTALLED_APPS and migrations are applied

#### Serializer Errors

- **Issue**: Missing fields in serializer response
- **Solution**: Check serializer field definitions and related field sources

#### Permission Errors

- **Issue**: 401 Unauthorized when expected to work
- **Solution**: Verify authentication setup and permission classes

### Test Output Example

```
Creating test database for alias 'default'...
Found 40 test(s).
System check identified no issues (0 silenced).
................E...
======================================================================
ERROR: test_retrieve_author_detail (api.test_views.AuthorAPITestCase.test_retrieve_author_detail)
Test retrieving a specific author
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/path/to/test_views.py", line 437, in test_retrieve_author_detail
    self.assertEqual(len(response.data['books']), 1)
                         ~~~~~~~~~~~~~^^^^^^^^^
KeyError: 'books'
----------------------------------------------------------------------
Ran 40 tests in 5.107s
FAILED (failures=1, errors=14)
Destroying test database for alias 'default'...
```

## Best Practices

### Test Organization

- Group related tests in the same test class
- Use descriptive test method names
- Include docstrings explaining what each test does

### Test Data

- Use realistic test data
- Create minimal test data needed for each test
- Clean up test data in `tearDown()` if necessary

### Assertions

- Use specific assertions (e.g., `assertEqual`, `assertIn`)
- Test both success and failure cases
- Verify response status codes and data content

### Authentication

- Use appropriate authentication methods for API testing
- Test both authenticated and unauthenticated scenarios
- Verify permission enforcement

## Maintenance

### Adding New Tests

1. Identify the functionality to test
2. Create appropriate test data in `setUp()`
3. Write test methods with descriptive names
4. Include both positive and negative test cases
5. Run tests to ensure they pass

### Updating Tests

- Update tests when API endpoints change
- Modify test data when model fields change
- Adjust assertions when response format changes

### Debugging Failed Tests

1. Run the specific failing test with verbose output
2. Check the test database state
3. Verify authentication and permissions
4. Review serializer and model definitions
5. Check URL patterns and view configurations

## Conclusion

This comprehensive testing suite ensures the integrity of the Django REST Framework APIs by testing:

- CRUD operations
- Authentication and permissions
- Filtering, searching, and ordering
- Data validation
- Model relationships

The tests provide confidence that the API behaves correctly under various conditions and inputs, ensuring reliable functionality for API consumers.
