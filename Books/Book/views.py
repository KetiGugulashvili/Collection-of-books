from django.shortcuts import render
from django.views import View
from .models import Book
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from .forms import BookForm
import requests
from django.core.exceptions import ValidationError
from datetime import datetime


class HomeView(View):
    def get(self, request):
        return render(request, 'home.html')


class BookCreateView(CreateView):
    model = Book
    form_class = BookForm
    template_name = 'create.html'
    success_url = '/books'


class BookListView(ListView):
    model = Book
    context_object_name = "books"
    template_name = 'list.html'

    def get_queryset(self):
        queryset = super().get_queryset()

        title = self.request.GET.get('title')
        author = self.request.GET.get('author')
        publication_language = self.request.GET.get('publication_language')
        from_year = self.request.GET.get('from_year')
        to_year = self.request.GET.get('to_year')

        if title:
            queryset = queryset.filter(title__icontains=title)
        if author:
            queryset = queryset.filter(author__icontains=author)
        if publication_language:
            queryset = queryset.filter(publication_language__icontains=publication_language)
        if from_year:
            queryset = queryset.filter(publication_date__year__gte=from_year)
        if to_year:
            queryset = queryset.filter(publication_date__year__lte=to_year)

        return queryset


class BookDetailView(DetailView):
    model = Book
    context_object_name = "book"
    template_name = 'detail.html'


class BookUpdateView(UpdateView):
    model = Book
    form_class = BookForm
    template_name = 'update.html'
    success_url = '/books'


class BookDeleteView(DeleteView):
    model = Book
    success_url = '/books'


class BookImportView(View):
    def get(self, request):
        return render(request, 'book_import.html')

    def post(self, request):
        keywords = request.POST.get('keywords')
        url = f'https://www.googleapis.com/books/v1/volumes?q={keywords}'
        response = requests.get(url)
        response.raise_for_status()

        data = response.json()
        books = []

        for item in data.get('items', []):
            try:
                volume_info = item.get('volumeInfo', {})

                book = {
                    'title': volume_info.get('title', ''),
                    'author': volume_info.get('authors', []),
                    'publication_date': volume_info.get('publishedDate', ''),
                    'isbn_number': volume_info.get('industryIdentifiers', [{}])[0].get('identifier', ''),
                    'number_of_pages': volume_info.get('pageCount', 0),
                    'cover_link': volume_info.get('imageLinks', {}).get('thumbnail', ''),
                    'publication_language': volume_info.get('language', '')
                }

                books.append(book)

            except Exception as e:
                print(f"Error importing book: {str(e)}")

        self.save_books(books)
        return render(request, 'book_import.html', {'message': 'Books imported successfully.'})

    def save_books(self, books):
        for book in books:
            try:
                book_obj = Book(
                    title=book['title'],
                    author=', '.join(book['author']),
                    publication_date=self.parse_date(book['publication_date']),
                    isbn_number=book['isbn_number'],
                    number_of_pages=book['number_of_pages'],
                    cover_link=book['cover_link'],
                    publication_language=book['publication_language']
                )
                book_obj.full_clean()
                book_obj.save()
            except ValidationError as e:
                print(f"Validation error occurred: {str(e)}")
            except Exception as e:
                print(f"Error saving book: {str(e)}")

    @staticmethod
    def parse_date(date):
        if len(date) == 4:
            publ = datetime.strptime(date, '%Y').date().replace(month=1, day=1)
        else:
            publ = datetime.strptime(date, '%Y-%m-%d').date()
        return publ

