from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import logout

# Create your views here.
def main(request):
    return render(request, 'main.html')

def detailview(request):
    return render(request, 'detailview.html')
def products(request):
    return render(request, 'products.html')
def custom_logout(request):
    logout(request)
    return redirect('/')