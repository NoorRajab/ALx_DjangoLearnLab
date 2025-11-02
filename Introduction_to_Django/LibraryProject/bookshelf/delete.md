retrieved_book = Book.objects.get(title="Nineteen Eighty-Four")
retrieved_book.delete()

print(list(Book.objects.all()))
