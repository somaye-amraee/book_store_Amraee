from django.contrib.auth import get_user_model
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django_countries.fields import CountryField


class Address(models.Model):
    class Meta:
        verbose_name = 'ادرس'
        verbose_name_plural = 'ادرس ها'

    state = models.CharField(verbose_name='استان', max_length=200)
    city = models.CharField(verbose_name='شهر', max_length=200)
    street = models.CharField(verbose_name='خیابان1',max_length=200)
    street_2 = models.CharField(verbose_name='خیابان2',max_length=200)
    detail_adress = models.CharField(verbose_name='جزییات آدرس',max_length=200, blank=True, null=True)
    postal_code = models.CharField(verbose_name='کد پستی',max_length=100)


    def __str__(self):
        return f' {self.state},{self.city}, {self.street} '

class CustomUser(AbstractUser):
    # username = models.CharField(verbose_name= 'نام کاربری', max_length=250, null=True, blank=True)
    email = models.EmailField(verbose_name='ایمیل', max_length=250, unique=True, null=True)
    is_customer = models.BooleanField(verbose_name='مشتری', default=False)
    is_staff = models.BooleanField(verbose_name='کارمند', default=False)
    is_superuser = models.BooleanField(verbose_name='ادمین',default=False)
    first_name = models.CharField(verbose_name='نام', max_length=200, null=True, blank=True)
    last_name = models.CharField(verbose_name='نام خانوادگی', max_length=200, null=True, blank=True)
    company = models.CharField(max_length=200)
    address = models.ManyToManyField(Address)
    phone = models.IntegerField(null=True, blank=True)
    fax = models.IntegerField(null=True, blank=True)
    is_active = models.BooleanField(verbose_name='فعال', default=True)
    last_login = models.DateTimeField(verbose_name='آخرین ورود', null=True, blank=True)


    # def __str__(self):
    #     return f'{self.first_name} {self.last_name}'

    def register(self):
        self.save()

    @staticmethod
    def get_customer_by_email(email):
        try:
            return CustomUser.objects.get(email=email)
        except:
            return False

    def isExists(self):
        if CustomUser.objects.filter(email=self.email):
            return True

        return False

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

class CustomerProxy(CustomUser):
    class Meta:
        proxy = True

class StaffProxy(CustomUser):
    class Meta:
        proxy = True
        # permissions=['']

class AdminProxy(CustomUser):
    class Meta:
        proxy = True

    # Create your models here.

    # class UserManager(BaseUserManager):
    #     def create_user(self, email, password, is_staff, is_superuser,):
    #         if not email:
    #             raise ValueError('you must have a valid email')
    #         now = timezone.now()
    #         email = self.normalize_email(email)
    #         user = self.model(email=email, is_staff=is_staff, is_active=True, is_superuser=is_superuser,
    #                           last_login=now, date_joined=now)
    #         user.set_password(password)
    #         user.save(using=self.db)
    #         return user
    #
    #     def create_superuser(self, email, password):
    #         user = self.create_user(email, password, True, True,)
    #         user.save(using=self.db)
    #         return user

    # def set_default_group(self):
    #     return self.groups.set(['مشتری'])

    # class CustomGroup(Group):
    #     class Meta:
    #         verbose_name= "گروه کاربری"
    #         verbose_name_plural = "گروههای کاربری"

    # USERNAME_FIELD = 'email'
    # EMAIL_FIELD = 'email'
    # REQUIRED_FIELDS = []
    # objects = UserManager()

    # def get_absolute_url(self):
    #     return "/users/%i/" % self.pk


# class CustomerProxy(CustomUser):
#     class Meta:
#         proxy = True
#         verbose_name= 'مشتری'
#         verbose_name_plural= 'مشتری ها'
#
#
#     class StaffProxy(CustomUser):
#         class Meta:
#             proxy = True
#             verbose_name = 'کارمند'
#             verbose_name_plural = 'کارمندها'
#
#
#     class AdminProxy(CustomUser):
#         class Meta:
#             proxy = True
#             verbose_name = 'ادمین'
#             verbose_name_plural = 'ادمین ها'





