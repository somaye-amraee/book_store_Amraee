
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *
from .forms import UserRegisterForm
admin.site.register(Address)


class CustomUserAdmin(UserAdmin):
    add_form = UserRegisterForm
    model = CustomUser
    list_display = ['email', 'username','id']
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('phone',)}),
    )


admin.site.register(CustomUser, CustomUserAdmin)


@admin.register(CustomerProxy)
class CustomerAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        return CustomUser.objects.filter(is_staff=False,is_superuser=False)
    list_display = ['email','username']


@admin.register(StaffProxy)
class StaffAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        return CustomUser.objects.filter(is_staff=True,is_superuser=False)

    list_display = ['email', 'username']


@admin.register(AdminProxy)
class AdminAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        return CustomUser.objects.filter(is_staff=True,is_superuser=True)

    list_display = ['email', 'username']

admin.site.register(Profile)