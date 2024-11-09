from django.db import models

# Create your models here.
class Author(models.Model):
    name = models.CharField(max_length=100)

class Books(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(Author,on_delete=models.CASCADE,related_name='books')

class Library(models.Model):
    name = models.CharField(max_length=100)
    books = models.ManyToManyField(Books,related_name='library')

class Librarian(models.Model):
    name = models.CharField(max_length=100)
    library = models.OneToOneField(Library, related_name='librarian')