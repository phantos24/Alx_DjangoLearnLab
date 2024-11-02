from bookshelf.models import Book
book = Book.Objects.get(title="1984")
book.title = "Nineteen Eighty-Four"
book.save()