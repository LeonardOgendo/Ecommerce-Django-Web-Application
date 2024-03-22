from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import logout

# Create your views here.

def custom_logout(request):
    logout(request)
    return redirect('/')