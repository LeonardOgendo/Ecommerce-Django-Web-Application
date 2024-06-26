from django.db import models
from django.conf import settings

from django.contrib.auth.models import User
from django.shortcuts import reverse


class Item(models.Model):
    item_image = models.ImageField(upload_to='images/', null=True)
    title = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=0)
    description = models.TextField(null=True)
    descimage1 = models.ImageField(upload_to='images/', null=True)
    descimage2 = models.ImageField(upload_to='images/', null=True)
    descimage3 = models.ImageField(upload_to='images/', null=True)
    slug = models.SlugField()
    item_status = models.CharField(max_length=10, choices=(('featured', 'Featured'), ('latest', 'Latest')), null=True)
    item_category = models.CharField(max_length=20, choices=(('clothing&footwear', 'Clothing & Footwear'), ('electronics', 'Electronics')), null=True)
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('Core:itemdetailview', kwargs={
            'slug':self.slug
        })    
    
    def get_add_to_cart_url(self):
        return reverse("Core:add-to-cart", kwargs={
            'slug':self.slug
        })
    
    def get_remove_from_cart_url(self):
        return reverse("Core:remove-from-cart", kwargs={
            'slug':self.slug
        })

class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    size = models.CharField(max_length=10, null=True)
    size_category = models.CharField(max_length=10, null=True)
    
    def __str__(self):
        return f"{self.quantity} of {self.item.title}"
    
    def get_total_item_price(self):
        return self.quantity * self.item.price
    
    #This is so that on the Order model, i can calculate a total
    def get_final_price(self):
        return self.get_total_item_price()

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)
    checkout_details = models.ForeignKey('CheckoutDetail', on_delete=models.SET_NULL, null=True, blank=True)
    
    def __str__(self):
        return self.user.username
    
    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_final_price()
        return total
    

class CustomerDetail(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100, null=True)
    country = models.CharField(max_length=100)
    town = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    pickup_station = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.first_name} {self.surname}"
    
class CheckoutDetail(models.Model):
    customer_details = models.ForeignKey('CustomerDetail', on_delete=models.SET_NULL, null=True, blank=True)
    payment_option = models.TextField()
    
    def __str__(self):
        return f"{self.customer_details.first_name} - {self.customer_details.pickup_station}"
    