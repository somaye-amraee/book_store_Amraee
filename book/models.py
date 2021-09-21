from django.db import models
from django.urls import reverse
from django_extensions.db.fields import AutoSlugField
from discount.models import ProductDiscount



class BookManager(models.Manager):
    """
    یک منیجر برای گرفتن کتابهای فعال
    """

    def get_active_books(self):
        return self.get_queryset().filter(active=True)


class Category(models.Model):
    """
    یک مدل برای دسته بندی
    """
    class Meta:
        verbose_name = 'دسته بندی'
        verbose_name_plural = "دسته بندی ها"

    name = models.CharField(verbose_name='دسته بندی ها', max_length=200, default='')
    slug = AutoSlugField(max_length=200, allow_unicode=True, populate_from=['id', 'name', ], unique=True)

    @staticmethod
    def get_all_categories():
        return Category.objects.all()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('list_category', args=[str(self.slug)])


class Author(models.Model):
    """
   مدل نویسنده
    """
    class Meta:
        verbose_name = 'نویسنده'
        verbose_name_plural = "نویسندگان"

    full_name = models.CharField(verbose_name='نام نام خانوادگی', max_length=200)

    def __str__(self):
        return self.full_name
    def get_absolute_url(self):
        return reverse('author_listadmin', args=[str(self.id)])


class Book(models.Model):
    """
        مدل کتاب و فیلدهای مربوطه
    """
    class Meta:
        verbose_name = 'کتاب'
        verbose_name_plural = 'کتاب ها'

    title = models.CharField(verbose_name='عنوان', max_length=200)
    description = models.TextField('توضیحات', max_length=500)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    created_at = models.DateTimeField('تاریخ ثبت', auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    inventory = models.PositiveIntegerField('انبار', default=0)
    unit_price = models.PositiveIntegerField('قیمت', default=0)
    discount = models.ForeignKey(ProductDiscount, on_delete=models.DO_NOTHING, null=True, blank=True)
    total_price = models.PositiveIntegerField()
    image = models.ImageField(upload_to='book_pic/', default='./images/default_pic.png')
    document_addr = models.FileField(upload_to='documents/', blank=True, null=True)
    slug = AutoSlugField(max_length=200, allow_unicode=True, populate_from=['id', 'title', 'author'], unique=True)
    available = models.BooleanField(verbose_name='موجود/ناموجود', default=True)

    """
    متد محاسبه قیمت
    """
    @property
    def total_price(self):
        if not self.discount:
            return self.unit_price
        elif self.discount.discount_type == 'P':
            if self.discount.active == True:
                total = (self.discount.percent_discount * self.unit_price) / 100
                return int(self.unit_price - total)
            else:
                print('the discount is expired')
                return self.unit_price

        elif self.discount.discount_type == 'C':
            if self.discount.active == True:
                return self.unit_price-self.discount.cash_discount
            else:
                print('the discount is expired')
                return self.unit_price
        return self.total_price



    @staticmethod
    def get_products_by_id(ids):
        return Book.objects.filter (id__in=ids)
    @staticmethod
    def get_all_products():
        return Book.objects.all()

    @staticmethod
    def get_all_products_by_categoryid(category_id):
        if category_id:
            return Book.objects.filter (category=category_id)
        else:
            return Book.get_all_products()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('book_detail', args=[str(self.slug)])

