from django.contrib.auth import authenticate, login, logout
from django.views.generic import FormView, View
from django.utils.translation import gettext_lazy as _
from django.shortcuts import redirect, reverse
from .mixins import LogoutRequiredMixin
from django.urls import reverse_lazy
from .models import User, Profile
from .otp import OtpManager
from . import forms


# Render LoginView
class LoginView(LogoutRequiredMixin, FormView):
    template_name = "account/login_template.html"
    form_class = forms.LoginForm

    def get_success_url(self):
        # Get next_url from url and override the success_url
        next_url = self.request.GET.get("next")
        if not next_url:
            next_url = reverse_lazy("main:index")

        return next_url

    def form_valid(self, form):
        data = form.cleaned_data
        login(request=self.request, user=data)
        
        return super(LoginView, self).form_valid(form)


# Render RegisterView
class RegisterView(LogoutRequiredMixin, FormView):
    template_name = "account/register_template.html"
    form_class = forms.RegisterForm

    def get_success_url(self):
        # Get next_url from url and override the success_url
        next_url = reverse_lazy("account:otp_check")
        if not next_url:
            next_url = reverse_lazy("account:otp_check")

        return next_url

    def form_valid(self, form):
        data = form.cleaned_data

        # Try to get existing user or create a new
        try:
            user = User.objects.get(mobile=data.get("mobile"), verified=False)
        except User.DoesNotExist:
            user = User.objects.create_user(mobile=data.get("mobile"), password=data.get("password1"))

        # Create new otp and send via sms
        otp = OtpManager(user.mobile)
        otp.create_otp(self.request)

        return super(RegisterView, self).form_valid(form)


# Render MobileFormView
class MobileFormView(LogoutRequiredMixin, FormView):
    template_name = "account/mobile_form_template.html"
    form_class = forms.MobileForm


class OtpCheckView(LogoutRequiredMixin, FormView):
    template_name = "account/otp_template.html"
    form_class = forms.OtpCheckForm

    def get_success_url(self):
        # Get next_url from url and override the success_url
        next_url = self.request.GET.get("next")
        if not next_url:
            next_url = reverse("main:index")
        return next_url

    def form_valid(self, form):
        data = form.cleaned_data
        user_otp = OtpManager(token=self.request.session.get("otp_token"))

        if data == user_otp.otp.otp:
            user = User.objects.get(mobile=user_otp.otp.mobile)
            user.verified = True
            user.save()

            login(self.request, user, backend="django.contrib.auth.backends.ModelBackend")  # Login user
            user_otp.delete_otp(self.request)  # Delete method
        else:
            form.add_error("number_one", _("Invalid code"))

        return super(OtpCheckView, self).form_valid(form)


# Render LogoutView(func)
def logout_view(request):
    if request.user.is_authenticated:
        logout(request)

    next_url = request.GET.get("next")  # Get next_url from url path
    if not next_url:
        # Return to home page if next_url not exists
        next_url = reverse("main:index")

    return redirect(next_url)
