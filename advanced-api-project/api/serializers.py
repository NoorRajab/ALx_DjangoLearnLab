
from rest_framework import serializers
from .models import Author, Book
from datetime import date

class BookSerializer(serializers.ModelSerializer):
    """
    Serializer for the Book model. It includes custom validation for the publication year.
    """
    class Meta:
        model = Book
        fields = ['id', 'title', 'publication_year', 'author']
        read_only_fields = ['author'] # Prevent accidental modification of the foreign key directly

    def validate_publication_year(self, value):
        """
        Custom validation to ensure the publication_year is not in the future.
        """
        current_year = date.today().year
        if value > current_year:
            raise serializers.ValidationError(f"Publication year cannot be in the future. Current year is {current_year}.")
        return value

class AuthorSerializer(serializers.ModelSerializer):
    """
    Serializer for the Author model.
    It includes a nested BookSerializer to display all books related to the author.
    """
    # The 'books' field matches the related_name defined in Book.author field.
    # setting many=True tells the serializer to expect a queryset/list of Book objects.
    books = BookSerializer(many=True, read_only=True)

    class Meta:
        model = Author
        fields = ['id', 'name', 'books'] # 'books' field displays the nested Book data

    # Documentation Requirements:
    # 1. Relationship Handling: The AuthorSerializer handles the one-to-many 
    #    relationship by including the 'books' field, which is defined as a 
    #    nested BookSerializer with many=True. This automatically fetches 
    #    all related Book instances via the 'books' related_name and serializes 
    #    them when an Author instance is requested.