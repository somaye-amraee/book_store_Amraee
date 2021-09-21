from django.contrib import admin

# Register your models here.
from django.contrib import admin

# Register your models here.
from .models import Author,Book,Category


@admin.register(Book)
class AdminBook(admin.ModelAdmin):
    # list_display = [
    #
    #     'id','title','slug','inventory','unit_price','discount_type','available','total_price',
    # ]
    list_display = [

        'id','title','slug','inventory','unit_price','discount','total_price','available',
    ]
    list_editable = ['unit_price','inventory','discount','available']


@admin.register(Category)
class AdminCategory(admin.ModelAdmin):
    list_display = [
        'name','slug'
    ]


@admin.register(Author)
class AdminAuthor(admin.ModelAdmin):
    list_display = [
        'full_name',
    ]

