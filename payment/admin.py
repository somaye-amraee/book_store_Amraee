from django.contrib import admin
from .models import *


class ItemInLine(admin.TabularInline):
    model = ItemOrder
    readonly_fields = ['customer', 'product', 'quantity']


class OrderAdmin(admin.ModelAdmin):
    list_display = ['id','customer','email','l_name','address','paid','get_price']


admin.site.register(Order,OrderAdmin)
admin.site.register(ItemOrder)
