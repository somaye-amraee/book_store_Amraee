
from django.contrib import admin
from .models import *
# Register your models here.


class CartAdmin(admin.ModelAdmin):
    list_display = ['id','customer', 'product', 'quantity']


admin.site.register(Cart, CartAdmin)

