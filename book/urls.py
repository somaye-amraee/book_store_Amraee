from django.urls import path
from .views import *
urlpatterns = [
    # book
    path('book/list', BookListView.as_view(), name='listbook'),
    path('', home, name='home'),
    path('adminlistbook/', BookListViewAdmin.as_view(), name='booklistadmin'),
    path('books/<slug>', BookDetailView,name='book_detail'),
    path('booksbytitle/', SearchBookByTitle, name='book_title'),
    path('book/new/',BookCreateView.as_view(), name='book_new'),
    path('book/<int:pk>/edit/', BookUpdateView.as_view(), name='book_edit'),
    path('book/<int:pk>/delete/', BookDeleteView.as_view(), name='book_delete'),

    # author
    path('authorlistbook/', AuthorListViewAdmin.as_view(), name='author_listadmin'),
    path('author/new/', AuthorCreateView.as_view(), name='author_new'),
    path('author/<int:pk>/delete/', AuthorDeleteView.as_view(), name='author_delete'),

    # category
    path('category/new/', CategoryCreateView.as_view(), name='category_new'),
    path('category/list/',  CategoryListViewAdmin.as_view(), name='list_category'),
    path('category/<int:pk>/delete/', CategoryDeleteView.as_view(), name='category_delete'),

    ]

