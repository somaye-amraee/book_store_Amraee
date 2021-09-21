from django.db import models
from django.utils import timezone


class Discount(models.Model):
    """
    a base model for the other discount models
    """
    DISCOUNT_CHOICES = [('C', 'مقداری'), ('P', 'درصدی'),('S','امتیازی')]
    discount_type = models.CharField(choices=DISCOUNT_CHOICES, default='C', max_length=5)
    cash_discount = models.PositiveIntegerField(verbose_name='مقدار تخفیف نقدی',  default=0)
    percent_discount = models.PositiveIntegerField(verbose_name='مقدار تخفیف درصدی', default=0)
    star_discount = models.PositiveIntegerField('تخفیف امتیازی',default=0)
    validate_date = models.DateTimeField(verbose_name='تاریخ اعمال کد تخفیف', )
    expire_date = models.DateTimeField(verbose_name='تاریخ اعتبار کد تخفیف', )
    active = models.BooleanField('وضعیت تخفیف', default=False)

    class Meta:
        abstract = True

    def active_status(self):
        if self.expire_date <= timezone.now():
            self.active = False
            self.save()
        return self.active


class BasketDiscount(Discount):
    """
    تخفیه روی سبد
    """
    class Meta:
        verbose_name = 'تخفیف کددار'
        verbose_name_plural = 'تخفیف های کددار'

    code_discount = models.CharField(verbose_name='کد تخفیف', max_length=100, unique=True)

    def _str_(self):
        return f'The deadline of discount  {self.id} is {self.expire_date}'


class ProductDiscount(Discount):
    """
    تخفیف روی کتاب
    """

    class Meta:
        verbose_name = 'تخفیف کتاب'
        verbose_name_plural = 'تخفیف هایکتاب'

    title = models.CharField('نام تخفیف نقدی', max_length=100, unique=True)
    max_purchase = models.IntegerField(verbose_name='سقف تخفیف', default=0)

    def _str_(self):
        return f'{self.title}'
