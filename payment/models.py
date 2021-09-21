from django.db import models
from accounts.models import CustomUser, Address
from book.models import Book



class Order(models.Model):
    """
    مدل سفارشات
    """
    class Meta:
        verbose_name = 'سفارش'
        verbose_name_plural = 'سفارش های  کاربران'

    customer = models.ForeignKey(CustomUser, verbose_name='مشتری',
                                on_delete=models.CASCADE, related_name='customers')
    address= models.CharField(max_length=150)
    email = models.EmailField()
    f_name = models.CharField(max_length=50)
    l_name = models.CharField(max_length=50)
    discount_code = models.PositiveIntegerField(blank=True,null=True)
    create_date = models.DateTimeField(verbose_name='زمان ایجاد سفارش', auto_now_add=True)
    quantity = models.IntegerField(default=1)
    paid = models.BooleanField(default=False, verbose_name='تکمیل خرید')

    def __str__(self):
        return f'{self.customer.last_name} | {self.create_date}  '

    def get_price(self):
        total = sum(i.price() for i in self.order_item.all())
        if self.discount_code:
            discount_price = (self.discount_code/100) * total
            return int(total - discount_price)
        return total


class ItemOrder(models.Model):
    """
    مدل جزییات سفارش
    """
    class Meta:
        verbose_name = 'ایتم سفارش'
        verbose_name_plural = 'ایتم های سفارش'
    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE,related_name='order_item', verbose_name='سبد خرید')
    product = models.ForeignKey(Book, on_delete=models.CASCADE, verbose_name='محصول')
    quantity = models.IntegerField(verbose_name='تعداد', default=0)

    def __str__(self):
        return f'{self.customer.last_name} {self.order.create_date}'

    def price(self):
        return self.product.total_price * self.quantity
