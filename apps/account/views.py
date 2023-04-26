from django.views.generic import FormView, TemplateView, View
from django.contrib.auth import authenticate, login, logout
from django.utils.translation import gettext_lazy as _
from django.shortcuts import redirect, reverse
from .mixins import LogoutRequiredMixin
from django.urls import reverse_lazy
from .models import User, Profile
from .otp import otp_random_code
from . import forms


# Render LoginView(Form)
class LoginView(LogoutRequiredMixin, FormView):
    template_name = 'account/login.html'
    form_class = forms.LoginForm
    success_url = reverse_lazy('main:index')

    def form_valid(self, form):
        cleaned_data = form.cleaned_data

        # Get user and authenticate it
        user = authenticate(self.request,username=cleaned_data.get('username'), password=cleaned_data.get('password'))
        login(self.request, user=user)  # Login user

        return super().form_valid(form)


# Render RegisterView(From)
class RegisterView(LogoutRequiredMixin, FormView):
    template_name = 'account/register.html'
    form_class = forms.RegisterForm
    success_url = reverse_lazy('account:otp_send')

    def form_valid(self, form):
        cleaned_data = form.cleaned_data

        # Check if user exists but not verified
        if User.objects.filter(mobile=cleaned_data['mobile'], verified=False).exists():
            user = User.objects.get(mobile=cleaned_data['mobile'], verified=False)  # Get not verified user
        else:
            user = User.objects.create_user(mobile=cleaned_data['mobile'], password=cleaned_data['password1'])  # Create new user

        self.request.session['user_id'] = user.id  # Save user_id in sessions

        return super().form_valid(form)


# Render MobileView(Form)
class MobileView(LogoutRequiredMixin, FormView):
    template_name = 'account/mobile_form.html'
    form_class = forms.MobileForm
    success_url = reverse_lazy('account:otp_send')

    def form_valid(self, form):
        cleaned_datta = form.cleaned_data

        user = User.objects.get(mobile=cleaned_datta['mobile'], verified=True)  # Get verified user
        self.request.session['user_id'] = user.id  # Save user_id in sessions

        return super().form_valid(form)


# Render OtpSendView(func)
def otp_send_view(request):
    if request.method == 'GET':
        user_id = request.session.get('user_id')  # Get user_id from session
        user = User.objects.get(id=user_id)  # Get user with query from database

        # Check if otp_token is exists
        if 'otp_token' in request.session:
            del request.session['otp_token']

        otp_token = otp_random_code(user.mobile)  # Create new random otp
        request.session['otp_token'] = otp_token  # Save otp_token in sessions

        return redirect('account:otp_check')  # Redirect to OtpCheck form

    else:
        return redirect('main:index')  # Redirect to index page if request is POST


# Render OtpCheckView(Form)
class OtpCheckView(LogoutRequiredMixin, FormView):
    template_name = 'account/otp_check.html'
    form_class = forms.OtpCheckForm
    success_url = reverse_lazy('main:index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if 'user_id' in self.request.session:
            user_id = self.request.session.get('user_id')  # Get user_id from sessions
            user = User.objects.get(id=user_id)  # Get user with query from database
        else:
            return context

        # Send mobile number and redirect url by the type of login(login or register)
        if user.verified is True:
            context['url'] = reverse('account:mobile')  # Set return url as 'mobile' page
        else:
            context['url'] = reverse('account:register')  # Set return url as 'register' page

        context['mobile'] = user.mobile  # Send mobile number

        return context

    def form_valid(self, form):
        cleaned_data = int(form.cleaned_data)
        otp_token = self.request.session.get('otp_token')

        if otp_token != cleaned_data:
            form.add_error('number_one', _('Entered otp is not correct'))  # Raise error if user code is not correct
            return super().form_invalid(form)

        user_id = self.request.session.get('user_id')  # Get user_id
        user = User.objects.get(id=user_id)  # Get user from database

        # Check for type of login(login or register)
        if user.verified is False:
            user.verified = True  # Verify new user and save it
            user.save()

        login(self.request, user=user, backend='django.contrib.auth.backends.ModelBackend')  # Login user

        # Delete user_id from session
        if 'user_id' in self.request.session:
            del self.request.session['user_id']

        # Delete otp_token from session
        if 'otp_token' in self.request.session:
            del self.request.session['otp_token']

        return super().form_valid(form)


# Render LogoutView(func)
def logout_view(request):
    if request.user.is_authenticated:
        logout(request)

    return redirect('main:index')
