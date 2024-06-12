from django.urls import path
from .import views

app_name = 'Payments'

urlpatterns = [
    path('payments/m-pesa', views.mpesa, name='m-pesa'),
    path('payments/paypal', views.paypal, name='paypal')
]
