from bookshelf.models import Book

book_to_delete = Book.objects.get(title="Nineteen Eighty-Four")

book_pk = book_to_delete.pk

book_to_delete.delete()

print(list(Book.objects.filter(pk=book_pk)))
