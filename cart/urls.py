from django.urls import path
from .views import *
urlpatterns = [
    path('', cart_detail,name='cart_detail'),
    path('add/<int:id>/', add_cart,name='add_cart'),
    path('remove/<int:id>/', remove_cart,name='remove_cart'),
    path('add_single/<int:id>/',add_single,name='add_single'),
    path('remove_single/<int:id>/',remove_single,name='remove_single'),