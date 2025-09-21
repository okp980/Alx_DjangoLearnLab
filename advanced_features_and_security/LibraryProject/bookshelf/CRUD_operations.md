# Django CRUD Operations Documentation

This document contains comprehensive CRUD (Create, Read, Update, Delete) operations performed in the Django shell for the LibraryProject.

## Prerequisites

Before running these operations, ensure you're in the correct directory and have Django shell running:

```bash
cd Introduction_to_Django/LibraryProject
python manage.py shell
```

## Import the Book Model

First, import the Book model in the Django shell:

```python
from bookshelf.models import Book
```

---

## CREATE Operations

### 1. Creating a Single Book Object

**Command:**

```python
book = Book.objects.create(title="1984", author="George Orwell", publication_year=1949)
book.save()
```

**Expected Output:**

```python
>>> book = Book.objects.create(title="1984", author="George Orwell", publication_year=1949)
>>> book.save()
>>> book.id
1
```

### 2. Creating Multiple Books

**Command:**

```python
# Create multiple books
book1 = Book.objects.create(title="To Kill a Mockingbird", author="Harper Lee", publication_year=1960)
book2 = Book.objects.create(title="The Great Gatsby", author="F. Scott Fitzgerald", publication_year=1925)
book3 = Book.objects.create(title="Pride and Prejudice", author="Jane Austen", publication_year=1813)
```

**Expected Output:**

```python
>>> book1 = Book.objects.create(title="To Kill a Mockingbird", author="Harper Lee", publication_year=1960)
>>> book2 = Book.objects.create(title="The Great Gatsby", author="F. Scott Fitzgerald", publication_year=1925)
>>> book3 = Book.objects.create(title="Pride and Prejudice", author="Jane Austen", publication_year=1813)
>>> book1.id
2
>>> book2.id
3
>>> book3.id
4
```

---

## READ Operations

### 1. Retrieve a Single Book by ID

**Command:**

```python
book = Book.objects.get(id=1)
```

**Expected Output:**

```python
>>> book = Book.objects.get(id=1)
>>> book
<Book: Book object (1)>
>>> book.title
'1984'
>>> book.author
'George Orwell'
>>> book.publication_year
1949
```

### 2. Retrieve All Books

**Command:**

```python
all_books = Book.objects.all()
```

**Expected Output:**

```python
>>> all_books = Book.objects.all()
>>> all_books
<QuerySet [<Book: Book object (1)>, <Book: Book object (2)>, <Book: Book object (3)>, <Book: Book object (4)>]>
>>> for book in all_books:
...     print(f"ID: {book.id}, Title: {book.title}, Author: {book.author}, Year: {book.publication_year}")
...
ID: 1, Title: 1984, Author: George Orwell, Year: 1949
ID: 2, Title: To Kill a Mockingbird, Author: Harper Lee, Year: 1960
ID: 3, Title: The Great Gatsby, Author: F. Scott Fitzgerald, Year: 1925
ID: 4, Title: Pride and Prejudice, Author: Jane Austen, Year: 1813
```

### 3. Filter Books by Author

**Command:**

```python
orwell_books = Book.objects.filter(author="George Orwell")
```

**Expected Output:**

```python
>>> orwell_books = Book.objects.filter(author="George Orwell")
>>> orwell_books
<QuerySet [<Book: Book object (1)>]>
>>> orwell_books.first().title
'1984'
```

### 4. Filter Books by Publication Year Range

**Command:**

```python
modern_books = Book.objects.filter(publication_year__gte=1900)
```

**Expected Output:**

```python
>>> modern_books = Book.objects.filter(publication_year__gte=1900)
>>> modern_books
<QuerySet [<Book: Book object (1)>, <Book: Book object (2)>, <Book: Book object (3)>]>
>>> for book in modern_books:
...     print(f"{book.title} ({book.publication_year})")
...
1984 (1949)
To Kill a Mockingbird (1960)
The Great Gatsby (1925)
```

### 5. Order Books by Publication Year

**Command:**

```python
books_by_year = Book.objects.order_by('publication_year')
```

**Expected Output:**

```python
>>> books_by_year = Book.objects.order_by('publication_year')
>>> for book in books_by_year:
...     print(f"{book.title} - {book.publication_year}")
...
Pride and Prejudice - 1813
The Great Gatsby - 1925
1984 - 1949
To Kill a Mockingbird - 1960
```

---

## UPDATE Operations

### 1. Update a Single Book

**Command:**

```python
book = Book.objects.get(id=1)
book.title = "Nineteen Eighty-Four"
book.save()
```

**Expected Output:**

```python
>>> book = Book.objects.get(id=1)
>>> book.title = "Nineteen Eighty-Four"
>>> book.save()
>>> book.title
'Nineteen Eighty-Four'
```

### 2. Update Multiple Books Using Filter

**Command:**

```python
Book.objects.filter(author="George Orwell").update(publication_year=1948)
```

**Expected Output:**

```python
>>> Book.objects.filter(author="George Orwell").update(publication_year=1948)
1
>>> Book.objects.get(id=1).publication_year
1948
```

### 3. Update All Books (Add a prefix to titles)

**Command:**

```python
for book in Book.objects.all():
    book.title = f"Classic: {book.title}"
    book.save()
```

**Expected Output:**

```python
>>> for book in Book.objects.all():
...     book.title = f"Classic: {book.title}"
...     book.save()
>>> Book.objects.all().values_list('title', flat=True)
<QuerySet ['Classic: Nineteen Eighty-Four', 'Classic: To Kill a Mockingbird', 'Classic: The Great Gatsby', 'Classic: Pride and Prejudice']>
```

---

## DELETE Operations

### 1. Delete a Single Book

**Command:**

```python
book = Book.objects.get(id=4)
book.delete()
```

**Expected Output:**

```python
>>> book = Book.objects.get(id=4)
>>> book.delete()
(1, {'bookshelf.Book': 1})
>>> Book.objects.count()
3
```

### 2. Delete Multiple Books Using Filter

**Command:**

```python
Book.objects.filter(author="F. Scott Fitzgerald").delete()
```

**Expected Output:**

```python
>>> Book.objects.filter(author="F. Scott Fitzgerald").delete()
(1, {'bookshelf.Book': 1})
>>> Book.objects.count()
2
```

### 3. Delete All Books

**Command:**

```python
Book.objects.all().delete()
```

**Expected Output:**

```python
>>> Book.objects.all().delete()
(2, {'bookshelf.Book': 2})
>>> Book.objects.count()
0
```

---

## Additional Useful Operations

### 1. Count Total Books

**Command:**

```python
Book.objects.count()
```

**Expected Output:**

```python
>>> Book.objects.count()
4
```

### 2. Check if Books Exist

**Command:**

```python
Book.objects.filter(author="George Orwell").exists()
```

**Expected Output:**

```python
>>> Book.objects.filter(author="George Orwell").exists()
True
```

### 3. Get First and Last Books

**Command:**

```python
first_book = Book.objects.first()
last_book = Book.objects.last()
```

**Expected Output:**

```python
>>> first_book = Book.objects.first()
>>> first_book.title
'1984'
>>> last_book = Book.objects.last()
>>> last_book.title
'Pride and Prejudice'
```

### 4. Complex Queries

**Command:**

```python
# Books published between 1900 and 1950
mid_century_books = Book.objects.filter(publication_year__gte=1900, publication_year__lte=1950)
```

**Expected Output:**

```python
>>> mid_century_books = Book.objects.filter(publication_year__gte=1900, publication_year__lte=1950)
>>> for book in mid_century_books:
...     print(f"{book.title} ({book.publication_year})")
...
1984 (1949)
The Great Gatsby (1925)
```

---

## Summary

This documentation covers all basic CRUD operations:

- **CREATE**: Creating single and multiple book objects
- **READ**: Retrieving books by ID, filtering, ordering, and complex queries
- **UPDATE**: Updating single and multiple books
- **DELETE**: Deleting single, multiple, and all books

Each operation includes the exact commands to run in the Django shell and the expected outputs. These operations demonstrate the power and flexibility of Django's ORM for database operations.
