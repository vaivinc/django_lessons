from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from captcha.fields import CaptchaField


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    captcha = CaptchaField()

    class Meta:
        model = User
        extra_fields = ['email']
        fields = ["username", "password1", "password2"]