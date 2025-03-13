from django.contrib import admin
from django.urls import path
from .views import index, about

urlpatterns = [
    path('home/', index, name="index"),
    path('about/', about, name="about")
]
