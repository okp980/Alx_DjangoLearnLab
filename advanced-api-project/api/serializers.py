from pyexpat import model
from rest_framework import serializers
from api.models import Author, Book

""" Serializers are used to convert model instances to JSON so that the frontend can work with the data. """


class AuthorSerializer(serializers.ModelSerializer):
    """ Serializer for the Author model 
    
    Args:
        serializers.ModelSerializer: The base class for model serializers.
        
    Attributes:
        model: The model that the serializer is based on.
        fields: The fields that the serializer will serialize.
    """
    books = serializers.StringRelatedField(source='book_set', many=True, read_only=True)
    class Meta:
        model = Author
        fields = ['id', 'name', 'books']
        
        
class BookSerializer(serializers.ModelSerializer):
    """ Serializer for the Book model 
    
    Args:
        serializers.ModelSerializer: The base class for model serializers.
        
    Attributes:
        model: The model that the serializer is based on.
        fields: The fields that the serializer will serialize.
        validate: The method that validates the data.
    """
    class Meta:
        model = Book
        fields = ['id', 'title', 'publication_year', 'author']
        
    """ Validates the publication year """
    def validate(self, attrs):
        if attrs['publication_year'] < 1000 or attrs['publication_year'] > 2024:
            raise serializers.ValidationError("Publication year must be between 1000 and 2024")
        return attrs