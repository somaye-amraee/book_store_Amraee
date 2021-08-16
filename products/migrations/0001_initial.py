# Generated by Django 3.2.4 on 2021-08-16 13:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=200)),
            ],
            options={
                'verbose_name': 'نویسنده',
                'verbose_name_plural': 'نویسندگان',
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(max_length=200)),
            ],
            options={
                'verbose_name': 'دسته بندی',
                'verbose_name_plural': 'دسته بندی ها',
            },
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='عنوان کتاب')),
                ('description', models.CharField(max_length=500, verbose_name='توضیحات کتاب')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ثبت')),
                ('inventory', models.IntegerField(default=0, verbose_name='موجودی انبار')),
                ('price', models.IntegerField(default=0, verbose_name='قیمت کتاب')),
                ('image', models.ImageField(default='default_pic.png', upload_to='book_pic/')),
                ('active', models.BooleanField(default=False, verbose_name='فعال / غیرفعال')),
                ('author', models.ForeignKey(max_length=150, on_delete=django.db.models.deletion.CASCADE, to='products.author', verbose_name='نام نویسنده')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.category', verbose_name='دسته بندی')),
            ],
            options={
                'verbose_name': 'کتاب',
                'verbose_name_plural': 'کتاب ها',
                'ordering': ('created',),
            },
        ),
    ]