from models import Author,Book,Library,Librarian

author = Library.objects.get(name=library_name)
books = author.books.all()

all_books = Book.objects.all()

librarian = Librarian.objects.all()