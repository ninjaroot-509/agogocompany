from django.urls import path

from .views import *

urlpatterns = [
    path('', process_order, name='checkout'),
    path('transaction/success/', moncash_p_done, name='moncash_p_done'),
    path('request-refund/', RequestRefundView.as_view(), name='request-refund'),
]
