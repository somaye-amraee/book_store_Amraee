import os

from django.db import models



class Category(models.Model):
    category = models.CharField(max_length=200)

    def _str_(self):
        return self.category


class Book(models.Model):
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=500)
    author = models.CharField(max_length=150)
    created_at = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    inventory = models.IntegerField('Inventory', default=0)
    price = models.IntegerField('Price', default=0)
    image = models.ImageField(upload_to='book_pic/', default='default_pic.png')
    document_address = models.FileField(upload_to='documents/')
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


class Author(models.Model):
    full_name = models.CharField(max_length=200)

    def __str__(self):
        return self.full_name