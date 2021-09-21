from django.urls import path

from .views import *
urlpatterns = [
    path('discount/new/', DiscountCreateView.as_view(), name='discount_new'),
    path('discount/list/', DiscountListViewAdmin.as_view(), name='discount_view_list'),
    path('discount/<int:pk>/edit/', DiscountUpdateView.as_view(), name='discount_edit'),
    path('discount/<int:pk>/delete/', DiscountDeleteView.as_view(), name='discount_delete'),
    path('<int:pk>/',
    DiscountDetailView.as_view(), name='discount_detail'),

]