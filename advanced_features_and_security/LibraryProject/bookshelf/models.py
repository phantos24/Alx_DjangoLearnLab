from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import BaseUserManager

# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length = 200)
    author = models.CharField(max_length = 100)
    publication_year = models.IntegerField(default=0000)

class CustomUser(AbstractUser):
    date_of_birth = models.DateField(null=True, blank=True)
    profile_photo = models.ImageField()

class CustomUserManager(BaseUserManager):
    def create_user(self, date_of_birth, profile_photo):
        CustomUser.date_of_birth = date_of_birth
        CustomUser.profile_photo = profile_photo
    
    def create_superuser(self, )