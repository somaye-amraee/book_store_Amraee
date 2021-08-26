from django.http import Http404
from django.shortcuts import render
from django.db.models import Q
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
    # context_object_name = 'books_all'
    context_object_name = 'products'


class BookDetailView(DetailView):
    model = Book
    template_name = 'book_detail.html'
    context_object_name = 'books_obj'


class BookSlugDetailView(DetailView):
    model = Book
    template_name = 'book_detail.html'
    context_object_name = 'books_obj'


def Book_detail_view(request, productId=None, *args, **kwargs):

    qs = Book.objects.filter(id=productId)
    print(qs)
    if qs.exists() and qs.count() == 1:
        product = qs.first()
    else:
        raise Http404("product does not found from try except")


    context = {
        "books_obj": product
    }

    return render(request, "book_detail.html", context)




"""
search data by title
"""




def SearchBookByTitle(request):
    q = request.GET['query']
    products=Book.objects.filter(Q(title__icontains=q) | Q(author__full_name__icontains=q))
    mydictionary = {
        "products" :products,
    }
    return render(request,'index.html',context=mydictionary)


