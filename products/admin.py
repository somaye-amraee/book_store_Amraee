from django.contrib import admin

from .models import Book,Category,Author
# Register your models here.

@admin.register(Book)
class AdminBook(admin.ModelAdmin):
    list_display = [

        'id','title','slug','inventory','unit_price','active'
    ]
    list_editable = ['active','unit_price','inventory']


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
