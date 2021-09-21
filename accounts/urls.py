from django.urls import path
from .views import *

urlpatterns = [
    # path('home/',home,name='home'),
    path('register/', user_register, name='user_register'),
    # path('register/staff/',staff_register, name='staff_register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('profile/',user_profile, name='profile'),
    path('profile/<int:pk>/edit/',UpdateProfile.as_view(),name='update'),
    path('profile/add/address/',AddressCreateView,name='add_address'),
    path('reset/pass/',ResetPassword.as_view(),name='reset'),
    path('reset/done/',ResetDonePassword.as_view(),name='reset_done'),
    path('active/<uidb64>/<token>/', RegisterEmail.as_view(), name='active'),
    path('confirm/<uidb64>/<token>/',ConfirmPassword.as_view(),name='password_resent_confirm'),
    path('confirm/done/', Complete.as_view(), name='complete'),
    path('change/',change_password,name='change'),
#     address
    path('address/', list_address, name='list_address'),
    # path('address/new/', AddressCreateView.as_view(), name='address_new'),
    path('address/new/', AddressCreateView, name='address_new'),
    path('book/<int:pk>/edit/', UpdateAddress.as_view(), name='address_edit'),
    path('book/<int:pk>/delete/', AddressDeleteView.as_view(), name='address_delete'),
    path('<int:pk>/',
        AddressDetailView.as_view(), name='address_detail'),

]

