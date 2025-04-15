from django.contrib import admin
from django.urls import path
from .views import index, about, products_details

app_name = "products"

urlpatterns = [
    path('index/', index, name="index"),
    path('about/', about, name="about"),
    path('products/<int:product_id>/', products_details, name="products_details")
]
