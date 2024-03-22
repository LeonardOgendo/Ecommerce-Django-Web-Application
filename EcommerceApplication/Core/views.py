from django.shortcuts import render
from .models import Item
from django.views.generic import ListView, DetailView
from django.utils import timezone
# Create your views here.
def main(request):
    return render(request, 'main.html')

class ProductsListView(ListView):
    model = Item
    template_name = 'products.html'

class ItemDetailView(DetailView):
    model = Item
    template_name = 'detailview.html'

def add_to_cart(request):
    pass