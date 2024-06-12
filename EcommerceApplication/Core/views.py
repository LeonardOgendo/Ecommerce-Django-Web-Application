from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from .models import Item, Order, OrderItem, CustomerDetail, CheckoutDetail
from django.views.generic import ListView, DetailView, View
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django_daraja.mpesa.core import MpesaClient
from django_countries import countries
import json
from django.urls import reverse
from django.conf import settings


# Create your views here.

def main(request):
    featured_items = Item.objects.filter(item_status='featured')
    latest_items = Item.objects.filter(item_status='latest')
    return render(request, 'main.html', {'featured_items':featured_items, 'latest_items':latest_items})

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
        
        # saving the selected size guide options
        if request.method == 'POST':
            size = request.POST.get('size')
            category = request.POST.get('size-category')
            
            # Save the selected size and category to the order item
            order_item.size = size
            order_item.size_category = category
            order_item.save()
            
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

class OrderSummaryView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            try:
                order = Order.objects.get(user=self.request.user, ordered=False)
                context = {
                    'object':order
                }
                return render(self.request, 'ordersummary.html', context) 
            except ObjectDoesNotExist:
                messages.error(self.request, "You do not have an active order.")
                return redirect('/')
        else:
            messages.error(request, "You are not logged in.")
            return redirect('account_login')

class CheckoutView(View):
    def get(self, request, *args, **kwargs):
        
        if request.user.is_authenticated:
            try:
                order = Order.objects.get(user=request.user, ordered=False)
                context = {
                    'customer_details':CustomerDetail.objects.get(user=request.user),
                    'object': order
                }
        
                return render(request, 'checkout.html', context)
            except ObjectDoesNotExist:
                messages.info(request, 'You do not have an active order.')
                return redirect('Core:productslistview')
        else:
            return redirect('account_login')
        
    def post(self, request, *ags, **kwargs):
        try:
            order = Order.objects.get(user=request.user, ordered=False)
            payment_method = request.POST.get('payment_method')
            customer_details = CustomerDetail.objects.get(user=request.user)
            if payment_method is not None:
                #save to backend
                checkout_details = CheckoutDetail(
                    customer_details = customer_details,
                    payment_option = payment_method
                )
                checkout_details.save()
                order.checkout_details = checkout_details
                order.save()
            
            # redirect to appropriate views.
                if payment_method == 'mpesa':
                    return redirect('Payments:m-pesa')
                elif payment_method == 'paypal':
                    return redirect('Payments:paypal')
                else:
                    # Handle other payment methods or unexpected values
                    messages.error(request, 'Unknown payment method selected')
                    return redirect('Core:checkout')
            else:
                messages.error(request, 'no payment option selected')
                return redirect('Core:checkout')
            
        except ObjectDoesNotExist:
            messages.info(request, "You don't have an active order.")
            return redirect('Core:productslistview')
def help_orderplacement(request):
    return render(request, 'help_orderplacement.html')

def help_payments(request):
    return render(request, 'help_payments.html')
 
def help_returns(request):
    return render(request, 'help_returns.html')
   


@login_required
def customer_details_view(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        surname = request.POST.get('surname')
        country_code = request.POST.get('country')
        country = dict(countries)[country_code]
        town = request.POST.get('town')
        phone_number = request.POST.get('phone_number')
        pickup_station = request.POST.get('pickup_station')

        customer = CustomerDetail.objects.get_or_create(
            user=request.user,
            first_name=first_name,
            surname=surname,
            country=country,
            town=town,
            phone_number=phone_number,
            pickup_station=pickup_station,
            
        )
        return redirect('Core:customer-details-view')

    return render(request, 'customerdetails.html', {'countries':countries})

def size_chart(request):
    return render(request, 'size_chart.html')

