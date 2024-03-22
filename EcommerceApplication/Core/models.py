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

class OrderItem(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.item.title

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)
    
    def __str__(self):
        return self.username