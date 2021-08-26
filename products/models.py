import os

from django.db import models
from django.urls import reverse
from django_extensions.db.fields import AutoSlugField


class BookManager(models.Manager):
    """
    a manager that will return active books
    """
    def get_active_books(self):
       return self.get_queryset().filter(active=True)

# دسته بندی محصولات
class Category(models.Model):
    category = models.CharField(max_length=200)
    class Meta:
        # verbose_name = 'دسته بندی'
        verbose_name_plural = 'دسته بندی ها'

    name = models.CharField(verbose_name='دسته بندی ها', max_length=200, default='')
    slug = AutoSlugField(max_length=200, allow_unicode=True, populate_from=['id', 'name', ], unique=True)

    @staticmethod
    def get_all_categories():
        return Category.objects.all()

    def __str__(self):
        return self.name

# مدل نویندگان
class Author(models.Model):
    full_name = models.CharField(max_length=200)
    class Meta:
        verbose_name = 'نویسنده'
        verbose_name_plural = 'نویسندگان'

    full_name = models.CharField(verbose_name='نام نام خانوادگی', max_length=200)

    def __str__(self):
        return self.full_name

# مدل محصول
class Book(models.Model):
    class Meta:
        verbose_name = 'کتاب'
        verbose_name_plural = 'کتاب ها'
        # ordering = ('created',)

    DISCOUNT_TYPE = [('P', 'Percentage'), ('C', 'Cash'), ('N', 'No Discount')]
    title = models.CharField(verbose_name='عنوان', max_length=200)
    description = models.CharField('توضیحات', max_length=500)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    created_at = models.DateTimeField('تاریخ ثبت', auto_now_add=True)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    inventory = models.PositiveIntegerField('انبار', default=0)
    image = models.ImageField(upload_to='book_pic/', default='static/images/default_pic.png')
    document_addr = models.FileField(upload_to='documents/', blank=True, null=True)
    active = models.BooleanField(default=False, verbose_name='فعال / غیرفعال')
    slug = AutoSlugField(max_length=200, allow_unicode=True, populate_from=['title', 'author', 'id'], unique=True)
    unit_price = models.PositiveIntegerField(default=0)
    discount_type = models.CharField('نوع تخفیف', choices=DISCOUNT_TYPE, null=True, blank=True, max_length=5,
                                     default='N')
    cash_discount = models.IntegerField(verbose_name='مقدار تخفیف نقدی', default=0)
    percent_discount = models.IntegerField(verbose_name='مقدار تخفیف درصدی', default=0)
    price = models.PositiveIntegerField('قیمت')


    def __str__(self):
        return self.title

    @staticmethod
    def get_products_by_id(ids):
        return Book.objects.filter(id__in=ids)

    @staticmethod
    def get_all_products():
        return Book.objects.all()

    @staticmethod
    def get_all_products_by_categoryid(category_id):
        if category_id:
            return Book.objects.filter(category=category_id)
        else:
            return Book.get_all_products()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('book_detail', args=[str(self.slug)])

    @property
    def price(self):
        if self.discount_type == 'N':
            return self.unit_price

        elif self.discount_type == 'C':

            return self.unit_price-self.cash_discount

        elif self.discount_type == 'P':
            total = (self.percent_discount * self.unit_price) / 100
            return int(self.unit_price - total)
        return self.price


