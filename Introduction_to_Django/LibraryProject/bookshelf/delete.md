from bookshelf.models import Book
book = Book.Objects.get(title="Nineteen Eighty-Four")
book.delete()
books = Book.objects.all()
