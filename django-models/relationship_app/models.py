from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class Author(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(Author,on_delete=models.CASCADE,related_name='books')

    class Meta(models.Model):
        permissions = ("can_add_book", "can_change_book", "can_delete_book")

    def __str__(self):
        return self.name

class Library(models.Model):
    name = models.CharField(max_length=100)
    books = models.ManyToManyField(Book,related_name='library')

    def __str__(self):
        return self.name

class Librarian(models.Model):
    name = models.CharField(max_length=100)
    library = models.OneToOneField(Library,on_delete=models.CASCADE,related_name='librarian')

    def __str__(self):
        return self.name
    
class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('Admin', 'Admin'),
        ('Librarian', 'Librarian'),
        ('Member', 'Member'),
    ]
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name='UserProfile')
    role = models.CharField(max_length=100,
                            choices=ROLE_CHOICES,
                            default='Member',)
    
    def __str__(self):
        return f"{self.user.username} - {self.role}"

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

