from django.contrib.auth import authenticate, login, logout
from django.views.generic import FormView
from django.utils.translation import gettext_lazy as _
from django.shortcuts import redirect, reverse
from .mixins import LogoutRequiredMixin
from django.urls import reverse_lazy
from .models import User, Profile
from threading import Thread
from .otp import random_otp
from . import forms


class LoginView(LogoutRequiredMixin, FormView):
    template_name = "account/login.html"
    form_class = forms.LoginForm

    def get_success_url(self):
        # Get next_url from url and override the success_url
        next_url = self.request.GET.get("next")
        if not next_url:
            next_url = reverse("main:index")

        return next_url

    def form_valid(self, form):
        data = form.cleaned_data
        login(request=self.request, user=data)
        
        return super(LoginView, self).form_valid(form)


# Render LogoutView(func)
def logout_view(request):
    if request.user.is_authenticated:
        logout(request)

    next_url = request.GET.get("next")  # Get next_url from url path
    if not next_url:
        # Return to home page if next_url not exists
        next_url = reverse("main:index")

    return redirect(next_url)
