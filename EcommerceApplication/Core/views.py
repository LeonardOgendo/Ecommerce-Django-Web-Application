from django.shortcuts import render, redirect, get_object_or_404
from .models import Item, Order, OrderItem
from django.views.generic import ListView, DetailView
from django.contrib import messages
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

def add_to_cart(request, slug):
    if not request.user.is_authenticated:
        return redirect('account_login')
    else:
        item = get_object_or_404(Item, slug=slug)
        order_item, created = OrderItem.objects.get_or_create(
            item=item,
            user=request.user,
            ordered=False
        )
        order_qs = Order.objects.filter(user=request.user, ordered=False)

        if order_qs.exists():
            order = order_qs[0]

            if order.items.filter(item__slug=item.slug).exists():
                order_item.quantity +=1
                order_item.save()
                messages.info(request, "This item quantity was updated.")
                
            else:
                order.items.add(order_item)
                messages.info(request, "This item was added to your cart.")
        else:
            ordered_date = timezone.now()
            order = Order.objects.create(user=request.user, ordered_date=ordered_date)
            order.items.add(order_item)
            messages.info(request, "This item was added to your cart.")
            
        return redirect("Core:itemdetailview", slug=slug)

def remove_from_cart(request, slug):
    if not request.user.is_authenticated:
        return redirect('account_login')
    else:
        item = get_object_or_404(Item, slug=slug)
        order_qs = Order.objects.filter(user=request.user, ordered=False)

        if order_qs.exists():
            order = order_qs[0]

            if order.items.filter(item__slug=item.slug).exists():
                order_item = OrderItem.objects.filter(
                    item=item,
                    user=request.user,
                    ordered=False
                )[0]
                if order_item.quantity > 1:
                    order_item.quantity -= 1
                    order_item.save()
                    messages.info(request, "This item quantity was updated.")
                else:
                    order_item.delete()
                    messages.info(request, "This item was removed from your cart.")
            else:
                messages.info(request, "This item was not in your cart.")
                return redirect('Core:itemdetailview', slug=slug)
        else:
            messages.info(request, "You do not have an active order")
            return redirect('Core:itemdetailview', slug=slug)

    return redirect('Core:itemdetailview', slug=slug)