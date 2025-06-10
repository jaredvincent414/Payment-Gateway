# payments/urls.py
from django.urls import path
from .views import InitiatePayment, RetrievePayment

urlpatterns = [
    path('v1/payments', InitiatePayment.as_view(), name='initiate-payment'),
    path('v1/payments/<int:pk>', RetrievePayment.as_view(), name='retrieve-payment'),
]
