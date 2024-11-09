from models import Author,Book,Library,Librarian

author = Author.objects.get(name=author_name)
books = author.objects.filter(author=author)

all_books = Library.objects.get(name=library_name)

librarian = Librarian.objects.all()