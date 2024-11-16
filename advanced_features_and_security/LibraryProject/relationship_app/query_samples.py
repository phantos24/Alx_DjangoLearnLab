from models import Author,Book,Library,Librarian

author = Author.objects.get(name=author_name)
books = author.objects.filter(author=author)

lib = Library.objects.get(name=library_name)
all_books = lib.books.all()

librarian = Librarian.objects.get(library=library_name)

