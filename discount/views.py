from django.shortcuts import render

# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, ListView, DetailView

from book.views import UserAccessMixin
from .models import BasketDiscount


class DiscountCreateView(UserAccessMixin, CreateView):
    """
            a cbv to create discount
            """
    permission_required = 'discount.add_BasketDiscount'
    permission_denied_message = ' sorry cant access to this page'
    model = BasketDiscount
    template_name = 'discount_new.html'
    fields = '__all__'


class DiscountDetailView(DetailView):
    model = BasketDiscount
    template_name = 'discount_detail.html'
    context_object_name = 'discount'


class DiscountUpdateView(UserAccessMixin, UpdateView):
    """
            a cbv to update BasketDiscount
            """
    permission_required = 'discount.change_BasketDiscount'
    permission_denied_message = ' sorry cant access to this page'
    model =BasketDiscount
    template_name = 'discount_edit.html'
    fields = '__all__'


class DiscountDeleteView(UserAccessMixin, DeleteView):
    """
            a cbv to delete discount
            """
    permission_required = 'discount.delete_BasketDiscount'
    permission_denied_message = ' sorry cant access to this page'
    model = BasketDiscount
    template_name = 'discount_delete.html'
    success_url = reverse_lazy('home')


class DiscountListViewAdmin(UserAccessMixin, ListView):
    """
     a cbv for list discount
     """
    permission_required = ('discount.delete_BasketDiscount', 'discount.change_BasketDiscount',
                           'discount.view_BasketDiscount')
    permission_denied_message = ' sorry cant access to this page'
    model = BasketDiscount
    template_name = 'discount_list.html'
    context_object_name = 'discounts'

