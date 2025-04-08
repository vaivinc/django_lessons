from django.contrib import admin
from django.urls import path
from .views import index, about, product_details

app_name = "shop"

urlpatterns = [
    path('index/', index, name="index"),
    path('about/', about, name="about"),
    path('product/<int:product_id>/', product_details, name="product_details")
]
