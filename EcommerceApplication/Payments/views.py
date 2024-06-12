from django.shortcuts import render
from .import views

# Create your views here.
def mpesa(request):
    return render(request, 'mpesa.html')

def paypal(request):
    return render(request, 'paypal.html')