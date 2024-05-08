from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from .models import Item, Order, OrderItem, CustomerDetail
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
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            customer_details = CustomerDetail.objects.get(user=self.request.user)
        except CustomerDetail.DoesNotExist:
            order = Order.objects.get(user=self.request.user, ordered=False)
            customer_details = None
        context = {
            'object': order,
            'customer_details': customer_details
        }
        return render(self.request, 'checkout.html', context)
    
def help_orderplacement(request):
    return render(request, 'help_orderplacement.html')

def help_payments(request):
    return render(request, 'help_payments.html')
 
def help_returns(request):
    return render(request, 'help_returns.html')
   
# mpesa api

def mpesa_payment(request):
    if request.method == 'POST':
        order = Order.objects.filter(user=request.user, ordered=False).first()
        customer = CustomerDetail.objects.filter(user=request.user).first()

        cl = MpesaClient()
        phone_number = customer.phone_number
        amount = int(order.get_total())

        account_reference = 'Africana_sales'
        transaction_desc = 'Africana products'

        callback_url = f'https://{settings.NGROK_DOMAIN}/{reverse("Core:stk_push_callback")}'
        response = cl.stk_push(phone_number, amount, account_reference, transaction_desc, callback_url)

        return HttpResponse(response)

    return HttpResponse('Method not allowed', status=405)

@login_required
def stk_push_callback(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            if data['Body']['stkCallback']['ResultCode'] == 0:
                # If the payment was successful update the order status,
                # send confirmation email to the user
                order = Order.objects.filter(user=request.user, ordered=False).first()
                if order:
                    order.ordered = True
                    order.save()
                    messages.success(request, 'Payment completed successfully.')
                    return redirect('Core:order-summary')
                else:
                    messages.error(request, 'Order not found.')
            else:
                messages.error(request, f'Error processing payment: {data["Body"]["stkCallback"]["ResultDesc"]}')
        except Exception as e:
            messages.error(request, 'Error processing payment: {}'.format(e))

        return HttpResponse('Payment not processed', status=400)

    return HttpResponse('Method not allowed', status=405)

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