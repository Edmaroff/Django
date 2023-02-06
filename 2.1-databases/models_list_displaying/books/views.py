from django.shortcuts import render, redirect
from books.models import Book
from django.core.paginator import Paginator


def redirect_view(request):
    response = redirect('books')
    return response


def books_view(request):
    template = 'books/books_list.html'
    books = Book.objects.order_by('pub_date')
    context = {'books': books}
    return render(request, template, context)


def composition_view(request, date):
    template = 'books/composition.html'
    compositions = Book.objects.order_by('pub_date').filter(pub_date=date)
    previous_book = Book.objects.order_by('pub_date').filter(pub_date__lt=date).first()
    next_book = Book.objects.order_by('pub_date').filter(pub_date__gt=date).first()
    context = {
        'compositions': compositions,
        'previous_book': previous_book,
        'next_book': next_book,
    }
    return render(request, template, context)
