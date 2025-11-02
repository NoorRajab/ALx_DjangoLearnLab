retrieved_book = Book.objects.get(title="1984")
print(retrieved_book.title)
print(retrieved_book.author)
print(retrieved_book.publication_year)
