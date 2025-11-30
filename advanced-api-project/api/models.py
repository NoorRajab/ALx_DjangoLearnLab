
from django.db import models

class Author(models.Model):
    """
    Model representing an Author.
    This model is the 'one' side of the one-to-many relationship with the Book model.
    """
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Book(models.Model):
    """
    Model representing a Book.
    It has a ForeignKey to Author, establishing the 'many' side of the relationship.
    This allows an Author to have multiple Books.
    """
    title = models.CharField(max_length=200)
    publication_year = models.IntegerField()
    # Foreign key to Author, setting up the one-to-many relationship.
    # on_delete=models.CASCADE means if an Author is deleted, all their Books are also deleted.
    author = models.ForeignKey(Author, related_name='books', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.title} ({self.publication_year})"