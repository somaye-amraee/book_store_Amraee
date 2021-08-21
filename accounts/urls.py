
# from django_countries.fields import CountryField
from django.urls import path

from .views import login_user, register, log_out

urlpatterns = [
    path('login', login_user),
    path('register', register),
    path('log-out', log_out)
]


