from django.contrib import admin
from .models import Book


class BooksAdmin(admin.ModelAdmin):
    list_display = ('title',)


admin.site.register(Book, BooksAdmin)
