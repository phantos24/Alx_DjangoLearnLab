from django.db import models

# Create your models here.
# Author model to represent authors
class Author(models.Model):
    name = models.CharField(max_length = 100)

    def __str__(self):
        return self.name
    
# book model connected with author for each book
class Book(models.Model):
    title = models.CharField(max_length = 100)
    publication_year = models.IntegerField()
    author = models.ForeignKey('Author',on_delete=models.CASCADE,related_name='books')

    def __str__(self):
        return self.title
    