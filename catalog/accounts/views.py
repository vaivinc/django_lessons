from django.contrib.messages.context_processors import messages
from django.http import HttpResponseBadRequest
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.core.mail import send_mail

from .forms import RegisterForm,  ProfileUpdateForm
from .models import Profile
from django.contrib.auth.models import User


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("shop:index")
    else:
        form = RegisterForm()
    return render(request, "register.html", context={"form": form})


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            next_url = request.GET.get('next')
            return redirect(next_url or 'shop:index')
        else:
            return render(request, 'login.html', context={'error': 'Incorrect login or password'})
    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect("shop:index")


@login_required
def profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    return render(request, "profile.html", {"profile": profile})


@login_required
def edit_profile_view(request):
    user = request.user
    profile, created = Profile.objects.get_or_create(user=request.user)
    if request.method == "POST":
            form = ProfileUpdateForm(request.POST, request.FILES, user=user)
            if form.is_valid():
                new_email = form.cleaned_data.get("email")
                # user.email = new_email
                # user.save()
                if new_email != user.email:
                    confirm_url = request.build_absolute_uri(reverse("confirm_email"))
                    confirm_url += f"?user={user.id}&email={new_email}"
                    subject = "Confirm new email"
                    message = f"Hello, {user.username} you want to change your email? " \
                              f"To confirm this operations click on link: {confirm_url}"
                    send_mail(subject, message, "noreply@gmail.com", [new_email], fail_silently=False)
                    messages.info(request, "Confirmation email was send")

                avatar = form.cleaned_data.get("avatar")
                if avatar:
                    profile.avatar = avatar
                profile.save()
    else:
        form = ProfileUpdateForm(user=user)
    return render(request, "edit_profile.html", context={"form": form, "user": user, "profile": profile})


def confirm_email(request):
    user_id = request.GET.get("user")
    new_email = request.GET.get("email")

    if not user_id or new_email:
        return HttpResponseBadRequest("Bad request no user or email")
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExists:
        return HttpResponseBadRequest("User not found")
    if User.objects.filter(email=new_email).exists():
        return HttpResponseBadRequest("This email already taken")
    user.email = new_email
    user.save()
    return render(request, "shop/confirm_email.html", {"new_email": new_email})

