from .models import Author, Book, Library, Librarian

# 1. List all books in Library
library_name = "Central Library"
library = Library.objects.get(name=library_name)
library.books.all()

# 2. Query all books by a specific author
author_name = "J.K. Rowling"
author = Author.objects.get(name=author_name)
books = Book.objects.filter(author=author)

# 3. Retrieve the librarian for a library
librarian = Librarian.objects.get(library=library)

