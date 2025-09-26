from django.db import models

# Create your models here.

class Author(models.Model):
    """ Model for the Author 
    
    Args:
        models.Model: The base class for models.
        
    Attributes:
        name: The name of the author.
    """
    name = models.CharField(max_length=100)


class Book(models.Model):
    """ Model for the Book 
    
    Args:
        models.Model: The base class for models.
        
    Attributes:
        title: The title of the book.
        publication_year: The publication year of the book.
        author: The author of the book.
    """
    title = models.CharField(max_length=100)
    publication_year = models.IntegerField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
  