from django.urls import path
from .views import *

urlpatterns = [
    path('<int:order_id>/',order_detail,name='order_detail'),
    path('create/',order_create,name='order_create'),
    path('coupon/<int:order_id>/',coupon_order,name='coupon_order'),
    path('history/',order_history,name='history'),

]