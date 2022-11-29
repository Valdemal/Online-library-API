from rest_framework import serializers

from .models import Book, Author


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ('id', 'title', 'year_of_writing', 'author', 'description', 'file', 'cover')


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ('name', 'surname', 'image', 'description', 'id')
