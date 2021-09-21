from django.shortcuts import render,redirect
from .models import *
from .forms import OrderForm,CouponForm
from cart.models import Cart
from discount.models import BasketDiscount
from django.views.decorators.http import require_POST
from django.utils import timezone
from django.contrib import messages



def order_detail(request, order_id):
    order = Order.objects.get(id=order_id)
    forms = CouponForm()
    return render(request, 'order.html', {'order': order, 'forms': forms})


"""
create 
cart == prod in cart get
delete when form checked
"""

# _____________________________________________
# @login_required(login_url='login')
def order_create(request):
    try:
        customer = request.user
    except:
        device = request.COOKIES['device']
        customer, created = CustomUser.objects.get_or_create(device=device)

    if request.method == 'POST':
        froms = OrderForm(request.POST)
        if froms.is_valid():
            data = froms.cleaned_data
            order = Order.objects.create(customer=customer, email=data['email'],
                                        f_name=data['f_name'], l_name=data['l_name'], address=data['address'])

            cart = Cart.objects.filter(customer=customer)
            for c in cart:
                ItemOrder.objects.create(order_id=order.id, customer_id=customer.id,
                                         product_id=c.product_id, quantity=c.quantity
                                         )
            Cart.objects.filter(customer_id=customer.id).delete()
            return redirect('order_detail', order.id)


"""
require_POST == if req is post
use when just post
check coupon
"""
@require_POST
def coupon_order(request,order_id):
    form = CouponForm(request.POST)
    time = timezone.now()
    if form.is_valid():
        code = form.cleaned_data['code']
        try:
            coupon = BasketDiscount.objects.get(code_discount__iexact=code,
                                                validate_date__lte=time, expire_date__gte=time, active=True)
        except BasketDiscount.DoesNotExist:
            messages.error(request, 'this code is not valid', 'danger')
            return redirect('order_detail', order_id)
        order = Order.objects.get(id=order_id)
        order.discount_code = coupon.percent_discount
        order.save()
    return redirect('order_detail', order_id)

# ----------------------------------------------------------------
"""
متد تاریخچه سفارشات
"""
def order_history(request):
    try:
        customer = request.user
    except:
        device = request.COOKIES['device']
        customer, created = CustomUser.objects.get_or_create(device=device)
    orders = Order.objects.filter(customer=customer)
    return render(request,'history.html',{'orders':orders})