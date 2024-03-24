from django.db import models
from django.conf import settings
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
    
    def __str__(self):
        return f"{self.quantity} of {self.item.title}"

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)   
    
    def __str__(self):
        return self.user.username