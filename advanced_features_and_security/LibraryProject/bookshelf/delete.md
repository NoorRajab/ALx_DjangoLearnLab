```python
from bookshelf.models import Book

book = Book.objects.get(title="Nineteen Eighty-Four")

book_pk = book.pk

book.delete()
print(list(Book.objects.filter(pk=book_pk)))

```
