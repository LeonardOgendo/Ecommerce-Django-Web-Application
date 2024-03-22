from django.urls import path
from . import views

app_name = 'Core'
urlpatterns = [
    path('', views.main, name='main'),
    path('products', views.ProductsListView.as_view(), name='productslistview'),
    path('detailview/<slug>/', views.ItemDetailView.as_view(), name='itemdetailview'),
    path('add-to-cart/<slug>/', views.add_to_cart, name='add-to-cart')
]