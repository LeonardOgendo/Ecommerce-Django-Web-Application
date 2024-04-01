from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from .models import Item, Order, OrderItem, CustomerDetail
from django.views.generic import ListView, DetailView, View
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django_daraja.mpesa.core import MpesaClient
from django_countries import countries

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

class OrderSummaryView(View):
    def get(self, *args, **kwargs):
        
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {
                'object':order
            }
            return render(self.request, 'ordersummary.html', context) 
        except ObjectDoesNotExist:
            messages.error(self.request, "You do not have an active order.")
            return redirect('/')

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
# mpesa api

def mpesa_payment(request):
    cl = MpesaClient()

    # Getting the current user's phone number from CustomerDetail model
    customer_detail = get_object_or_404(CustomerDetail, user=request.user)
    phone_number = customer_detail.phone_number

    # Get the total amount for the order
    order = Order.objects.filter(user=request.user, ordered=False).first()
    if order is None:
        return HttpResponse("No pending order found for this user", status=400)
    
    amount = order.get_total()

    account_reference = 'reference'
    transaction_desc = 'Description'
    callback_url = 'https://2541-196-250-209-176.ngrok-free.app'
    
    # Update order status
    order.ordered = True
    order.save()

    # Perform STK push
    response = cl.stk_push(phone_number, amount, account_reference, transaction_desc, callback_url)
    
    #return to the placed order view
    return HttpResponse(response)



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