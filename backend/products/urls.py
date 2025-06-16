from django.contrib import admin
from django.urls import path
from rest_framework.routers import DefaultRouter


from .views.category import CategoryViewSet
from .views.product import ProductViewSet
from .views.cart import CartViewSet

from .views.views import index, about, products_details, cart_add, delete_item_cart, checkout, cart_detail
from accounts.views.accounts import AccountViewSet

app_name = "products"

router = DefaultRouter()

router.register(r"products", viewset=ProductViewSet)
router.register(r"categories", viewset=CategoryViewSet, basename="categories")
router.register(r"carts", viewset=CartViewSet, basename="carts")
router.register(r"accounts", viewset=AccountViewSet, basename="accounts")

urlpatterns = [
    path('index/', index, name="index"),
    path('about/', about, name="about"),
    path('products/<int:product_id>/', products_details, name="products_details"),
    path("cart_add/<int:product_id>/", cart_add, name="cart_add"),
    path("products_details/", products_details, name="products_details"),
    path("delete_item_cart/", delete_item_cart, name="delete_item_cart"),
    path("checkout/", checkout, name="checkout"),
    path("cart_detail/", cart_detail, name="cart_detail")
]

urlpatterns += router.urls