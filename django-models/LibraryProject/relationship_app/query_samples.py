from .models import Author, Book, Library, Librarian

# 1. Get all books by an author
author = Author.objects.get(name="J.K. Rowling")
books = Book.objects.filter(author=author)
print(books)

# 2. Get all libraries that have a specific book
library_name = "Central Library"
library = Library.objects.get(name=library_name)
books = Book.objects.filter(library=library)
print(books)

# 3. Get all librarians that work in a specific library
librarian = Librarian.objects.get(library=library)
print(librarian)

# 4. Get all books that are in a specific library
books = Book.objects.filter(library=library)
print(books)