from models import Author,Book,Library,Librarian

author = Author.objects.get(name=author_name)

all_books = Library.objects.get(name=library_name)

librarian = Librarian.objects.all()