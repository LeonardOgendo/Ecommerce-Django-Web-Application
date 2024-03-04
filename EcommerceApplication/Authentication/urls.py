from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name='main'),
    path('detailview', views.detailview, name='detailview'),
    path('products', views.products, name='products'),
    path('logout', views.custom_logout, name='custom_logout')
]