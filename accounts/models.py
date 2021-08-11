from django.contrib.auth.models import AbstractUser
from django.db import models
from django_countries.fields import CountryField
# Create your models here.




class Address(models.Model):
    street = models.CharField(max_length=200)
    street_2 = models.CharField(max_length=200, blank=True, null=True)
    city = models.CharField(max_length=200)
    state = models.CharField(max_length=200)
    postal_code = models.CharField(max_length=100)
    country = CountryField()

    def __str__(self):
        return f' {self.country},{self.state},{self.city}, {self.street} '


class CustomUser(AbstractUser):
    is_customer = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    company = models.CharField(max_length=200)
    address = models.ManyToManyField(Address)
    phone = models.IntegerField(null=True, blank=True)
    fax = models.IntegerField(null=True, blank=True)



    def __str__(self):
        return f'{self.first_name} {self.last_name}'