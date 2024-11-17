from django.contrib import admin
from django.contrib.auth.models import Group

# Register your models here.
from .models import Book, CustomUser

class Bookadmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publication_year')
    list_filter = ('title', 'author', 'publication_year')
    search_fields = ('title', 'author', 'publication_year')

admin.site.register(Book, Bookadmin)

class CustomUserAdmin (admin.ModelAdmin):
    list_display = ('date_of_birth', 'profile_photo')

admin.site.register(CustomUser, CustomUserAdmin)

groups_data = {
    'Admin' : ["can_create","can_edit","can_view","can_delete"],
    'Editor' : ["can_edit","can_view"],
    'Viewers' : ["can_view"]
}