from django.urls import path
from .views import register, profile, logout_view, login_view, edit_profile_view, confirm_email

app_name = "shop"

urlpatterns = [
    path('register/', register, name="register"),
    path('profile/', profile, name="profile"),
    path('edit_profile/', edit_profile_view, name="edit_profile_view"),
    path('logout/', logout_view, name="logout"),
    path("login/", login_view, name="login"),
    path("confirm_email/", confirm_email, name="confirm_email")
]