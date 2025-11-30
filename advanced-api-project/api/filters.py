
import django_filters
from .models import Book

class BookFilter(django_filters.FilterSet):
    """
    Custom FilterSet for the Book model.
    Allows filtering by fields with specific lookup types.
    """
    # Filter by title containing the value (case-insensitive)
    title = django_filters.CharFilter(lookup_expr='icontains')
    
    # Filter by publication year (exact match)
    publication_year = django_filters.NumberFilter(lookup_expr='exact')
    
    # Filter by author name containing the value (via the foreign key relationship)
    # The 'author__name' syntax traverses the ForeignKey relationship.
    author_name = django_filters.CharFilter(field_name='author__name', lookup_expr='icontains')
    
    class Meta:
        model = Book
        # Fields available for default filtering (e.g., exact matches on author id)
        fields = ['title', 'publication_year', 'author', 'author_name']