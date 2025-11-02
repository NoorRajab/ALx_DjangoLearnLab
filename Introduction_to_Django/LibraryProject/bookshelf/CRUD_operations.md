from bookshelf.models import Book

book = Book.objects.create(title="1984", author="George Orwell", publication_year=1949)
retrieved_book = Book.objects.get(title="1984")
print(retrieved_book.title, retrieved_book.author, retrieved_book.publication_year)
retrieved_book.title = "Nineteen Eighty-Four"
retrieved_book.save()
print(Book.objects.get(pk=retrieved_book.pk).title)

retrieved_book.delete()

print(list(Book.objects.all()))
