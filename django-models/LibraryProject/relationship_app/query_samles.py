import os
import django
from django.db.models import Count

# Set up the Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_models.settings')
django.setup()

# Import the models
from relationship_app.models import Author, Book, Library, Librarian

def setup_data():
    """Populates the database with sample data."""
    print("--- Setting up sample data ---")

    # Clear previous data for a clean run
    Author.objects.all().delete()
    Library.objects.all().delete()
    
    # 1. Create Authors and Books (ForeignKey)
    author1 = Author.objects.create(name="J.R.R. Tolkien")
    author2 = Author.objects.create(name="Jane Austen")
    
    book1 = Book.objects.create(title="The Hobbit", author=author1)
    book2 = Book.objects.create(title="The Lord of the Rings", author=author1)
    book3 = Book.objects.create(title="Pride and Prejudice", author=author2)
    book4 = Book.objects.create(title="Emma", author=author2)

    # 2. Create Libraries and link Books (ManyToManyField)
    library_a = Library.objects.create(name="Central City Library")
    library_b = Library.objects.create(name="West Side Branch")
    
    # Add books to Library A
    library_a.books.add(book1, book2, book3)
    # Add a subset of books to Library B
    library_b.books.add(book3, book4)

    # 3. Create Librarians and link Libraries (OneToOneField)
    Librarian.objects.create(name="Alice Smith", library=library_a)
    Librarian.objects.create(name="Bob Johnson", library=library_b)
    
    print("Sample data populated successfully!")
    print("-" * 30)


def run_queries():
    """Executes the required queries."""
    
    # Define variables for query parameters
    author_name = "J.R.R. Tolkien"
    library_name_central = "Central City Library"
    library_name_west = "West Side Branch"
    
    # 1. Query all books by a specific author (ForeignKey relationship)
    print(f"### 1. Query all books by a specific author ({author_name}):")
    try:
        author = Author.objects.get(name=author_name)
        books_by_author = author.books.all()
        for book in books_by_author:
            print(f"- {book.title}")
    except Author.DoesNotExist:
        print(f"Author '{author_name}' not found.")
    print("-" * 30)
    
    # 2. List all books in a library (ManyToManyField relationship)
    print(f"### 2. List all books in a library ({library_name_central}):")
    try:
        # **CORRECTED LINE: Using variable library_name_central**
        library = Library.objects.get(name=library_name_central)
        books_in_library = library.books.all()
        for book in books_in_library:
            print(f"- {book.title}")
    except Library.DoesNotExist:
        print(f"Library '{library_name_central}' not found.")
    print("-" * 30)

    # 3. Retrieve the librarian for a library (OneToOneField relationship)
    print(f"### 3. Retrieve the librarian for a library ({library_name_west}):")
    try:
        # **CORRECTED LINE: Using variable library_name_west**
        library = Library.objects.get(name=library_name_west)
        librarian = library.librarian
        print(f"- The librarian is: {librarian.name}")
    except Library.DoesNotExist:
        print(f"Library '{library_name_west}' not found.")
    except Librarian.DoesNotExist:
        print("Librarian not found for this library.")
    print("-" * 30)


if __name__ == '__main__':
    setup_data()
    run_queries()