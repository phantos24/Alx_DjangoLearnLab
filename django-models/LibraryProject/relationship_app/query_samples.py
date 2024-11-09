from models import Author,Book,Librarian

author = Author.objects.get(name = "Mahmoud")
books = author.objects.all()

all_books = Book.objects.all()

librarian  = Librarian.objects.get()