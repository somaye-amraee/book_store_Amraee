from django.contrib import admin

# Register your models here.
from .models import Order, OrderDetail, BasketDiscount, ProductDiscount

# admin.site.register(Order)
admin.site.register(OrderDetail)
admin.site.register(BasketDiscount)
admin.site.register(ProductDiscount)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id','order_date','complete']