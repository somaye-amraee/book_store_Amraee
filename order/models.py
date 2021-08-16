from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone
from accounts.models import CustomUser
from products.models import Book
from django.contrib.auth.models import User

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
    # is_paid = models.BooleanField(verbose_name='پرداخت شده / نشده')
    # count = models.IntegerField(verbose_name='تعداد', default=1)
    # discount_cost = models.ForeignKey( ,verbose_name='تخفیف نقدی')
    order_date = models.DateTimeField(verbose_name='زمان ایجاد سفارش', auto_now_add= True )
    total_price=models.IntegerField(verbose_name='قیمت کل')
    total_discount = models.IntegerField(verbose_name='تخفیف کل')


    def __str__(self):
        return f'{self.id}'

    class OrderDetail(models.Model):
        class Meta:
            verbose_name = 'ایتم سفارش'
            verbose_name_plural = 'ایتم های سفارش'

        # STATUS_CHOICE = [('R', 'ثبت'), ('G', 'سفارش')]
        order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name='سبد خرید')
        book = models.ForeignKey(Book, on_delete=models.CASCADE, verbose_name='محصول')
        # price = models.IntegerField(verbose_name='قیمت محصول')
        count = models.IntegerField(verbose_name='تعداد')

        def __str__(self):
            return f'{self.id}'

    #
    # # total purchaces without discount
    # @property
    # def total_price(self):
    #     return sum(item.get_cost for item in self..all())
    #
    # @property
    # def total_discount(self):
    #     if self.discount_code.active and self.discount_code.status=='V':
    #         if self.discount_cost.max_purchase <=self.total_price:
    #             return self.discount_cost.cost - ((self.discount_code.percent / 100)* self.total_price)
    #         elif self.discount_code.active:
    #             return (self.discount_code.percent / 100) * self.total_price
    #         else:
    #             return 0





    # def __str__(self):
    #     return self.owner.get_full_name()





    # def __init__(self, *args, **kwargs):
    #     super().__init__(args, kwargs)
    #     self.orders = None
    #
    # def __str__(self):
    #     return self.book.title
    #
    # def final_order_price(self):
    #     orders_price = sum(self.orders.final_order_price())
    #     if self.discount:
    #         if self.discount.type =='Cash':
    #             return orders_price-self.discount.CashDiscount
    #         elif self.discount.type == 'PercentDiscount':
    #             return orders_price * (100- self.discount.p)/100
    #
    #     else:
    #         return orders_price





# class Order(models.Model):
#     customer = models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING, related_name='orders')
#     invoice_date = models.DateTimeField()
#     billing_address = models.CharField(max_length=70, blank=True, null=True)
#     billing_city = models.CharField(max_length=40, blank=True, null=True)
#     billing_state = models.CharField(max_length=40, blank=True, null=True)
#     billing_country = models.CharField(max_length=40, blank=True, null=True)
#     billing_postal_code = models.CharField(max_length=10, blank=True, null=True)
#     total = models.BigIntegerField()


# class OrderDetail(models.Model):
#     order = models.ForeignKey(Order, on_delete=models.PROTECT)
#     book = models.ForeignKey('products.Book', on_delete=models.DO_NOTHING)
#     unit_price = models.IntegerField()
#     quantity = models.IntegerField()