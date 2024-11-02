from bookshelf.models import Book
Book.Objects.get(title="Nineteen Eighty-Four").delete()
book = Book.objects.all()
