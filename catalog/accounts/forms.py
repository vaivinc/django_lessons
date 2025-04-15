from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from captcha.fields import CaptchaField
from django.core.exceptions import ValidationError


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    captcha = CaptchaField()

    class Meta:
        model = User
        extra_fields = ['email']
        fields = ["username", "password1", "password2", "email"]


class ProfileUpdateForm(forms.Form):
    email = forms.EmailField(label="Email:")
    avatar = forms.ImageField(required=False, label="Avatar:")

    def clean_email(self):
        new_email = self.cleaned_data.get("email")
        if User.objects.filter(email=new_email).exists():
            raise ValidationError("User with this Email Already Exists")
        else:
            return new_email