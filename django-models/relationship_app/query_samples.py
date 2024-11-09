from models import Author,Book,Library,Librarian

author = Author.objects.get(name="Mahmoud")
books = author.books.all()

all_books = Book.objects.all()

librarian = Librarian.objects.all()