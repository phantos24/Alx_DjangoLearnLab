from bookshelf.models import Book
Book.Objects.filter(title="1984").update(title="Nineteen Eighty-Four")