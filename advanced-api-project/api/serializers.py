from rest_framework import serializers
from .models import Book,Author
import datetime

# a serializer for books with a validation for publication year
class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'

    def validate_publication_year(self, value):
        current_year = datetime.datetime.now().year
        if value > current_year:
            raise serializers.ValidationError("The publication year cannot be in the future.")
        return value


# a serializer for authors with its connected book
class AuthorSerializer(serializers.ModelSerializer):
    books = BookSerializer(many = True, read_only = True)

    class Meta:
        model = Author
        fields = 'name'
