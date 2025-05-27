from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from . import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenObtainPairView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("products.urls", namespace="products")),
    path('accounts/', include('accounts.urls',  namespace="accounts")),
    path("captcha/", include("captcha.urls"))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += [
        path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
        path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
        path('api/token/', TokenObtainPairView.as_view(), name="token-obtain-pair"),
        path('api/token/refresh/', TokenObtainPairView.as_view(), name="token-refresh")
    ]