# payment/urls.py
from django.urls import path
from .views import MakePaymentView, RevertPaymentView

urlpatterns = [
    path('make-payment/', MakePaymentView.as_view(), name='make-payment'),
    path('revert-payment/', RevertPaymentView.as_view(), name='revert-payment'),
]
