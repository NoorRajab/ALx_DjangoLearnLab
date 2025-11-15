retrieved_book = Book.objects.get(title="1984") # Retrieve again if shell session was restarted
retrieved_book.title = "Nineteen Eighty-Four"
retrieved_book.save()
print(retrieved_book.title)
