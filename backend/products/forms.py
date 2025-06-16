from django import forms
from .models import Order
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class OrderCreateForm(forms.ModelForm):
    payment_method = forms.ChoiceField(choices={"liqpay": "With LiqPay",
                                                "monopay": "With MonoPay",
                                                "googlepay": "With Google Pay",
                                                "cash": "With Cash"
                                                }
                                       )
    class Meta:
        model = Order
        fields = ["contact_name", "contact_email", "contact_phone", "address"]
        labels = {"contact_name": "Your name",
                  "contact_email": "Your email",
                  "contact_phone": "Your phone",
                  "address": "Your address",
                  "payment_method": "Payment method"
                  }





