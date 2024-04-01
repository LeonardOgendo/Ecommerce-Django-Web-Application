from django.urls import path
from . import views

app_name = 'Core'
urlpatterns = [
    path('', views.main, name='main'),
    path('products', views.ProductsListView.as_view(), name='productslistview'),
    path('detailview/<slug>/', views.ItemDetailView.as_view(), name='itemdetailview'),
    path('add-to-cart/<slug>/', views.add_to_cart, name='add-to-cart'),
    path('remove-from-cart/<slug>/', views.remove_from_cart, name='remove-from-cart'),
    path('order-summary', views.OrderSummaryView.as_view(), name='order-summary'),
    path('checkout', views.CheckoutView.as_view(), name='checkout'),
    path('customer-details', views.customer_details_view, name="customer-details-view"),
    
    #MPESA API
    path('payment', views.mpesa_payment, name='mpesa-payment')
]