from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length = 200)
    author = models.CharField(max_length = 100)
    publication_year = models.IntegerField(default=0000)

class custom_fields(AbstractUser):
    date_of_birth = models.DateField(null=True, blank=True)
    profile_photo = models.ImageField()
