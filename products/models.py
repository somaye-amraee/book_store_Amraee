import os

from django.db import models


# دسته بندی محصولات
class Category(models.Model):
    category = models.CharField(max_length=200)
    class Meta:
        verbose_name = 'دسته بندی'
        verbose_name_plural = 'دسته بندی ها'

    def __str__(self):
        return self.category

# مدل نویندگان
class Author(models.Model):
    full_name = models.CharField(max_length=200)
    class Meta:
        verbose_name = 'نویسنده'
        verbose_name_plural = 'نویسندگان'

    def __str__(self):
        return self.full_name

# مدل محصول
class Book(models.Model):
    class Meta:
        verbose_name = 'کتاب'
        verbose_name_plural = 'کتاب ها'
        ordering = ('created',)

    title = models.CharField(verbose_name = 'عنوان کتاب', max_length=200)
    description = models.CharField(verbose_name = 'توضیحات کتاب',max_length=500)
    author = models.ForeignKey(Author,verbose_name = 'نام نویسنده',max_length=150, on_delete=models.CASCADE)
    created = models.DateTimeField(verbose_name = 'تاریخ ثبت',auto_now_add=True)
    category = models.ForeignKey(Category,verbose_name = 'دسته بندی', on_delete=models.CASCADE)
    inventory = models.IntegerField(verbose_name = 'موجودی انبار', default=0)
    price = models.IntegerField(verbose_name = 'قیمت کتاب', default=0)
    image = models.ImageField(upload_to='book_pic/', default='default_pic.png')
    active = models.BooleanField(default=False, verbose_name='فعال / غیرفعال')


    def __str__(self):
        return self.title

    def increment_inventory(self, amount):
        self.inventory += amount
        self.save()
        return f'the current value of {self.inventory}'

    def decrement_inventory(self, amount):
        self.inventory -= amount
        self.save()
        return f'the current value of {self.inventory}'

    def update_price(self, cash):
        self.price += cash
        self.save()

    def delete(self):
        deleted_obj = f'{self.title} deleted'
        self.delete()
        return deleted_obj


