from datetime import datetime

from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone
from accounts.models import CustomUser
from products.models import Book
from django.contrib.auth.models import User


class Discount(models.Model):
    """

    a base model for our other discount models
    """
    DISCOUNT_CHOICES = [('C', 'مقداری'), ('P', 'درصدی')]
    status = models.CharField(choices=DISCOUNT_CHOICES, default='C', max_length=5)
    cash_discount = models.IntegerField(verbose_name='مقدار تخفیف نقدی', blank=True, null=True)
    percent_discount = models.IntegerField(verbose_name='مقدار تخفیف درصدی', blank=True, null=True)
    validate_date = models.DateTimeField(verbose_name='تاریخ اعمال کد تخفیف', )
    expire_date = models.DateTimeField(verbose_name='تاریخ اعتبار کد تخفیف', )
    active = models.BooleanField('وضعیت تخفیف', default=False)

    class Meta:
        abstract = True

    def active_status(self):
        if self.expire_date < timezone.now():
            self.active = False
            self.save()

    def discount_apply(self):
        if self.validate_date == timezone.now():
            self.active = True
            self.save()


"""discountCode model which is both percent based and cash based"""
#  روی سبد خرید اعمال می شود
class BasketDiscount(models.Model):
    class Meta:
        verbose_name = 'تخفیف کددار'
        verbose_name_plural = 'تخفیف های کددار'

    DISCOUNT_CHOICES = [('C', 'مقدار'), ('P', 'درصدی')]
    status = models.CharField(choices=DISCOUNT_CHOICES, default='C', max_length=5)
    percent_discount = models.IntegerField(verbose_name='مقدار تخفیف درصدی', blank=True, null = True)
    cash_discount = models.IntegerField(verbose_name='مقدار تخفیف نقدی', blank=True, null = True)
    code_discount = models.CharField(verbose_name='کد تخفیف', max_length=100, blank=True, null=True)
    validate_date = models.DateTimeField(verbose_name='تاریخ اعمال کد تخفیف',)
    expire_date = models.DateTimeField(verbose_name='تاریخ اعتبار کد تخفیف', )
    active = models.BooleanField('وضعیت تخفیف',default=False)


    def __str__(self):
       return f'The discount deadline of {self.id} is {self.expire_date}'

    def update_active(self):
        if self.expire_date < timezone.now():
            self.active = False
            self.save()

    def apply_discount(self):
        if self.validate_date == timezone.now():
            self.active = True
            self.save()


# فقظ روی کتاب اعمال می شود
class ProductDiscount(models.Model):
    class Meta:
        verbose_name = 'تخفیف نقدی'
        verbose_name_plural = 'تخفیف های نقدی'

    DISCOUNT_CHOICES = [('C', 'مقدار'), ('P', 'درصدی')]
    status = models.CharField(choices=DISCOUNT_CHOICES, default='C', max_length=4)
    title = models.CharField('نام تخفیف نقدی', max_length=100, unique=True)
    cash_discount = models.IntegerField(verbose_name='مقدار تخفیف نقدی', blank=True, null = True)
    percent_discount = models.IntegerField(verbose_name='مقدار تخفیف درصدی',blank=True, null = True )
    max_purchase = models.DecimalField(verbose_name='سقف خرید',max_digits=10, decimal_places=4 , blank=True, null = True)
    validate_date = models.DateTimeField(verbose_name='تاریخ اعمال تخفیف',)
    expire_date = models.DateTimeField(verbose_name='تاریخ اعتبار تخفیف', )
    active = models.BooleanField('وضعیت تخفیف',default=False)
    book = models.ForeignKey(Book,on_delete=models.CASCADE)

    def __str__(self):
       return f'{self.title}'

    def update_active(self):
        if self.expire_date < timezone.now():
            self.active = False
            self.save()

    def apply_discount(self):
        if self.validate_date == timezone.now():
            self.active = True
            self.save()


# سفارش ها
class Order(models.Model):
    class Meta:
        verbose_name = 'سفارش'
        verbose_name_plural = 'سفارش های  کاربران'

    customer = models.ForeignKey(CustomUser,verbose_name='مشتری',related_name='orders', on_delete=models.CASCADE, )
    # discount = models.ForeignKey(CashDiscount, verbose_name='تخفیف نقدی', blank=True, null=True)
    discount_code = models.ForeignKey(BasketDiscount,on_delete=models.CASCADE,verbose_name= 'تخفیف کدی', max_length=100, blank=True, null=True)
    order_date = models.DateTimeField(verbose_name='زمان ایجاد سفارش', auto_now_add= True )
    total_price=models.IntegerField(verbose_name='قیمت کل')
    complete = models.BooleanField(default=False, verbose_name='تکمیل خرید')
    total_discount = models.IntegerField(verbose_name='تخفیف کل')


    def __str__(self):
        return self.customer.last_name

    def placeOrder(self):
        self.save()

    @staticmethod
    def get_orders_by_customer(customer_id):
        return Order.objects.filter(customer=customer_id).order_by('-order_date')


class OrderDetail(models.Model):
    class Meta:
        verbose_name = 'ایتم سفارش'
        verbose_name_plural = 'ایتم های سفارش'

    # STATUS_CHOICE = [('R', 'ثبت'), ('G', 'سفارش')]
    order = models.ForeignKey('Order', on_delete=models.CASCADE, verbose_name='سبد خرید')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, verbose_name='محصول')
    # price = models.IntegerField(verbose_name='قیمت محصول')
    count = models.IntegerField(verbose_name='تعداد')

    def __str__(self):
        return self.order.customer.last_name


    def get_total_item_price(self):
        total = self.book.price * self.quantity
        return total

    def get_total_discount_item_price(self):
        return self.quantity * self.book.discount_price

    def get_amount_saved(self):
        return self.get_total_item_price() - self.get_total_discount_item_price()

    def get_final_price(self):
        if self.book.discount_price:
            return self.get_total_discount_item_price()
        return self.get_total_item_price()











