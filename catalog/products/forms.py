from django import forms
from .models import Order


class OrderCreateForm(forms.ModelForm):
    payment_method = forms.ChoiceField(choices={"liqpay": "With LiqPay",
                                                "monopay": "With Monopay",
                                                "googlepay": "With Google Pay",
                                                "cash": "With cash"}, label="Payment method")

    class Meta:
        model = Order
        fields = ["contact_name", "contact_email", "contact_phone", "address"]
        labels = {"contact_name": "Your name", "contact_email": "Your email", "contact_phone": "Your phone",
                  "address": "Your address", "payment_method": "Payment method"}


