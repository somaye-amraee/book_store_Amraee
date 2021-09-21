from django.shortcuts import render
from msilib.schema import ListView
from django.shortcuts import render, redirect
from book.models import Book
from accounts.models import CustomUser
from .models import Cart, CartForm
from django.contrib.auth.decorators import login_required
from payment.forms import OrderForm

@login_required(login_url='login')
def cart_detail(request):
    try:
        customer = request.user


    except:
        device = request.COOKIES['device']
        customer, created = CustomUser.objects.get_or_create(device=device)

    cart = Cart.objects.filter(customer=customer)
    form = OrderForm()
    total = 0
    for pro in cart:
        total += pro.product.total_price * pro.quantity
    context= {
        'cart': cart, 'total': total, 'form': form,
    }
    return render(request, 'cart.html', context)


"""
اضافه کرن به کارت
1-باید بدانیم کدام محصول رو به سبد اضافه کنیم.
2. با فیلتر چک میکنیم که محصول قبلا در سبد بوده یا خیر.
3. اعتبار کاربر با ای دی چک میشود.
- check = 1 == yes exist already
- check = 0 == NO ==> create
4- customer chosed ==valid form to redirect
"""

@login_required(login_url='login')
def add_cart(request, id):
    url = request.META.get('HTTP_REFERER')
    product = Book.objects.get(id=id)

    try:
        customer = request.user

    except:
        device = request.COOKIES['device']
        customer, created = CustomUser.objects.get_or_create(device=device)


    data = Cart.objects.filter(customer=customer, product_id=product.id)
    if data:
        check = 1
    else:
        check = 0

    if request.method == 'POST':

        froms = CartForm(request.POST)
        if froms.is_valid():
            quan = froms.cleaned_data['quantity']
            if check == 1:
                shop = Cart.objects.get(customer=customer, product_id=id)
                shop.quantity += quan

            else:
                Cart.objects.create(customer=customer, product_id=id, quantity=quan)

        return redirect(url)


"""
حذف از سبد
"""
# @login_required(login_url='login')
def remove_cart(request, id):
    url = request.META.get('HTTP_REFERER')
    Cart.objects.filter(id=id).delete()
    return redirect(url)


"""
حذف و اضافه سینگل
"""
def add_single(request, id):
    url = request.META.get('HTTP_REFERER')
    cart = Cart.objects.get(id=id)
    product = Book.objects.get(id=cart.product.id)
    if product.inventory > cart.quantity:
        cart.quantity += 1
    cart.save()
    return redirect(url)


def remove_single(request,id):
    url = request.META.get('HTTP_REFERER')
    cart = Cart.objects.get(id=id)
    if cart.quantity <2:
        cart.delete()
    else:
        cart.quantity -= 1
        cart.save()
    return redirect(url)

# _______________________________________-
