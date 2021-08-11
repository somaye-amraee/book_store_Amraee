# from django.db import models
#
# # Create your models here.
# class Order(models.Model):
#     # owner = models.ForeignKey(User, on_delete=models.CASCADE)
#     order_number = models.IntegerField()
#     is_paid = models.BooleanField(verbose_name='پرداخت شده / نشده')
#     payment_date = models.DateTimeField(blank=True, null=True, verbose_name='تاریخ پرداخت')
#     order_item_count = models.IntegerField()
#     order_total = models.IntegerField()
#
#
#     class Meta:
#         verbose_name = 'سبد خرید'
#         verbose_name_plural = 'سبدهای خرید کاربران'
#
#     def __str__(self):
#         return self.owner.get_full_name()

#
# class OrderDetail(models.Model):
#     order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name='سبد خرید')
#     product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='محصول')
#     price = models.IntegerField(verbose_name='قیمت محصول')
#     count = models.IntegerField(verbose_name='تعداد')
#
#     class Meta:
#         verbose_name = 'جزییات محصول'
#         verbose_name_plural = 'اطلاعات جزییات محصولات'
#
#     def __str__(self):
#         return self.product.title

from django.db import models

# Create your models here.
from accounts.models import CustomUser


class Order(models.Model):
    customer = models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING, related_name='orders')
    invoice_date = models.DateTimeField()
    billing_address = models.CharField(max_length=70, blank=True, null=True)
    billing_city = models.CharField(max_length=40, blank=True, null=True)
    billing_state = models.CharField(max_length=40, blank=True, null=True)
    billing_country = models.CharField(max_length=40, blank=True, null=True)
    billing_postal_code = models.CharField(max_length=10, blank=True, null=True)
    total = models.BigIntegerField()


class OrderDetail(models.Model):
    order = models.ForeignKey(Order, on_delete=models.PROTECT)
    book = models.ForeignKey('products.Book', on_delete=models.DO_NOTHING)
    unit_price = models.IntegerField()
    quantity = models.IntegerField()