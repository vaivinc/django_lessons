from django.contrib import admin
from django.urls import path, include
from . import settings
from django.conf.urls.static import static

from products.views import cart_add, products_details

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("products.urls", namespace="products")),
    path('accounts/', include('accounts.urls',  namespace="accounts")),
    path("captcha/", include("captcha.urls")),
    path("cart_add/<int:product_id>/", cart_add, name="cart_add"),
    path("products_details/", products_details, name="products_details")
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)