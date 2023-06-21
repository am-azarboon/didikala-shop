from .mixins import LogoutRequiredMixin, ViewRedirectMixin
from django.utils.translation import gettext_lazy as _
from django.views.generic import FormView, View
from django.contrib.auth import login, logout
from django.shortcuts import redirect, reverse
from django.urls import reverse_lazy
from django.http import JsonResponse
from .models import User, Profile
from .otp import OtpManager
from . import forms


# Render LoginView
class LoginView(LogoutRequiredMixin, FormView):
    template_name = "account/login_template.html"
    form_class = forms.LoginForm
    success_url = reverse_lazy("main:index")

    def get_success_url(self):
        # Get next_url from url and override the success_url
        next_url = self.request.GET.get("next")
        if next_url:
            return next_url

        return super().get_success_url()

    def form_valid(self, form):
        data = form.cleaned_data  # Get user
        login(request=self.request, user=data)
        
        return super(LoginView, self).form_valid(form)


# Render RegisterView
class RegisterView(LogoutRequiredMixin, FormView):
    template_name = "account/register_template.html"
    form_class = forms.RegisterForm
    success_url = reverse_lazy("account:otp_check")

    def get_success_url(self):
        # Get next_url from url and override the success_url
        next_url = self.request.GET.get("next")
        if next_url:
            return reverse_lazy("account:otp_check") + f"?next={next_url}"

        return super().get_success_url()

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
    success_url = reverse_lazy("account:otp_check")

    def get_success_url(self):
        # Get next_url from url and override the success_url
        next_url = self.request.GET.get("next")
        if next_url:
            return reverse_lazy("account:otp_check") + f"?next={next_url}"

        return super().get_success_url()

    def form_valid(self, form):
        data = form.cleaned_data  # Get cleaned data (user.mobile)

        # Create new otp
        user_otp = OtpManager(mobile=data)
        user_otp.create_otp(self.request)

        return super(MobileFormView, self).form_valid(form)


class OtpCheckView(LogoutRequiredMixin, ViewRedirectMixin, FormView):
    template_name = "account/otp_template.html"
    form_class = forms.OtpCheckForm
    success_url = reverse_lazy("main:index")

    def get_success_url(self):
        # Get next_url from url and override the success_url
        next_url = self.request.GET.get("next")
        if next_url:
            return next_url

        return super().get_success_url()

    def form_valid(self, form):
        data = form.cleaned_data
        user_otp = OtpManager(token=self.request.session.get("otp_token"))

        # Check entered otp
        if data["otp_number"] == user_otp.otp.otp:
            user = User.objects.get(mobile=user_otp.otp.mobile)  # Get created user
            if not user.verified:
                user.verified = True  # Verify user
            user.save()

            login(self.request, user, backend="django.contrib.auth.backends.ModelBackend")  # Login user
            user_otp.delete_otp(self.request)  # Delete method
        else:
            form.add_error("otp_number", _("Invalid code"))  # Add error if Otp is not correct
            return super(OtpCheckView, self).form_invalid(form)

        return super(OtpCheckView, self).form_valid(form)


# Render ResendOtpView(json)
class ResendOtpView(LogoutRequiredMixin, View):
    def get(self, request):
        user_otp = OtpManager(token=request.session.get("otp_token"))
        user_otp.create_otp(request)

        return JsonResponse({"status": "sent"}, status=200)


# Render LogoutView(func)
def logout_view(request):
    if request.user.is_authenticated:
        logout(request)

    next_url = request.GET.get("next")  # Get next_url from url path
    if not next_url:
        # Return to home page if next_url not exists
        next_url = reverse("main:index")

    return redirect(next_url)
