from django.contrib import messages
from django.core.mail import send_mail
from django.urls import reverse
from django.template.loader import render_to_string
from django.conf import settings
from products.models import Order


def send_mail_confirm(request, user, new_email):
    confirm_url = request.build_absolute_uri(reverse("confirm_email"))
    confirm_url += f"?user={user.id}&email={new_email}"
    subject = "Confirm new email"
    message = f"Hello, {user.username} you want to change your email? " \
              f"To confirm this operations click on link: {confirm_url}"
    send_mail(subject,
              message,
              "noreply@gmail.com",
              [new_email],
              fail_silently=False
              )
    messages.info(request, "Confirmation email was send")


def send_order_confirmation_email(order: Order):
    subject = f"Confirmation order {order.id}"
    context = {"order": order}
    text_content = render_to_string(
        "email/confirmation_email.txt", context
    )
    to_email = order.contact_email
    try:
        send_mail(subject,
                  text_content,
                  settings.DEFAULT_FROM_EMAIL,
                  [to_email,
                   settings.ADMIN_EMAIL]
                  )
    except Exception as e:
        print(f"Error sending email: {e}")