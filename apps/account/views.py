from django.views.generic import FormView, TemplateView, View
from django.contrib.auth import authenticate, login, logout
from django.utils.translation import gettext_lazy as _
from django.shortcuts import redirect, reverse
from .mixins import LogoutRequiredMixin
from django.urls import reverse_lazy
from .models import User, Profile
from .otp import random_otp
from threading import Thread
from . import forms


# Render LogoutView(func)
def logout_view(request):
    if request.user.is_authenticated:
        logout(request)

    next_url = request.GET.get("next")  # Get next_url from url path
    if not next_url:
        # Return to home page if next_url not exists
        next_url = reverse("main:index")

    return redirect(next_url)
