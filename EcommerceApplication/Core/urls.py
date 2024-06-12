from django.urls import path
from .import views

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
    path('help/order-placement', views.help_orderplacement, name="help-orderplacement"),
    path('help/payments', views.help_payments, name='help-payments'),
    path('help/returns', views.help_returns, name="help-returns"),
    path('size-chart' ,views.size_chart, name='size-chart'),
]