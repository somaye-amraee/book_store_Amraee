from django.http import HttpResponseRedirect
from django.shortcuts import render , redirect

from django.contrib.auth.hashers import  check_password
from accounts.models import CustomUser
from django.views import View
from products.models import Book,Category
from .models import Order

 #
class Cart(View):
    def get(self , request):
        ids = list(request.session.get('cart').keys())
        products = Book.get_products_by_id(ids)
        print(products)
        return render(request,'cart.html', {'products': products})


class CheckOut(View):
    def post(self, request):
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        customer = request.session.get('customer')
        cart = request.session.get('cart')
        products = Book.get_products_by_id(list(cart.keys()))
        print(address, phone, customer, cart, products)

        for product in products:
            print(cart.get(str(product.id)))
            order = Order(customer=CustomUser(id=customer),
                              product=product,
                              price=product.price,
                              address=address,
                              quantity=cart.get(str(product.id)))
            order.save()
            # بعد از دادن آدرس و نهایی شدن خرید. کارت خالی می شود
        request.session['cart'] = {}

        return redirect('cart')

# برای اپدیت کردن تعداد محصولات
class Index(View):

    def post(self, request):
        product = request.POST.get('product')
        remove = request.POST.get('remove')
        cart = request.session.get('cart')
        if cart:
            quantity = cart.get(product)
            if quantity:
                if remove:
                    if quantity <= 1:
                        cart.pop(product)
                    else:
                        cart[product] = quantity - 1
                else:
                    cart[product] = quantity + 1

            else:
                cart[product] = 1
        else:
            cart = {}
            cart[product] = 1

        request.session['cart'] = cart
        print('cart', request.session['cart'])
        return redirect('homepage')

    def get(self, request):
        # print()
        return HttpResponseRedirect(f'/store{request.get_full_path()[1:]}')

# دسته بندی ها رو میگیره یعنی مثلا براساس دسته رمان کتاب ها رو نشون میده
def store(request):
    cart = request.session.get('cart')
    if not cart:
        request.session['cart'] = {}
    products = None
    categories = Category.get_all_categories()
    categoryID = request.GET.get('category')
    if categoryID:
        products = Book.get_all_products_by_categoryid(categoryID)
    else:
        products = Book.get_all_products()

    data = {}
    data['products'] = products
    data['categories'] = categories

    print('you are : ', request.session.get('email'))
    return render(request, 'index.html', data)

#   در   orderبرای نمایش اوردهایی که ثبت شده اند
class OrderView(View):

    def get(self , request ):
        customer = request.session.get('customer')
        orders = Order.get_orders_by_customer(customer)
        print(orders)
        return render(request , 'orders.html'  , {'orders' : orders})
