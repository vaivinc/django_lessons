from django.urls import path
from .views import register, profile, logout_view, login_view, edit_profile_view, confirm_email
from django.contrib.auth import views as auth_views

app_name = "shop"

urlpatterns = [
    path('register/', register, name="register"),
    path('profile/', profile, name="profile"),
    path('edit_profile/', edit_profile_view, name="edit_profile_view"),
    path('logout/', logout_view, name="logout"),
    path("login/", login_view, name="login"),
    path("confirm_email/", confirm_email, name="confirm_email"),
    path("password_reset/", auth_views.PasswordResetView.as_view(
        template_name="password_reset/form.html", email_template_name="password_reset/email.html", success_url="done/"
    ), name="password_reset"),
    path("password_reset/done/", auth_views.PasswordResetDoneView.as_view(
        template_name="password_reset/done.html"
    ), name="password_reset_done"),
    path("reset/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(
        template_name="password_reset/confirm.html"
    ), name="password_reset_confirm"),
    path("reset/done/", auth_views.PasswordResetCompleteView.as_view(
        template_name="password_reset/complete.html"
    ), name="password_reset_complete")
]