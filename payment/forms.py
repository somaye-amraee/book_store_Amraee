from django.forms import ModelForm
from .models import Order
from django import forms

class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = ['email','f_name','l_name','address']



class CouponForm(forms.Form):
    code = forms.CharField(max_length=100)
