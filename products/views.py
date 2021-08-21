from django.http import Http404
from django.shortcuts import render

from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Book
# Create your views here.


def home(request):
    """
    homepage loading method
    """
    return render(request, 'home.html')


class BookListView(ListView):
    # paginate_by = 2
    model = Book
    template_name = 'all_books.html'
    queryset = Book.objects.order_by('-created_at')
    context_object_name = 'books_all'
