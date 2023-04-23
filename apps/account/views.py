from django.views.generic import FormView, TemplateView, View
from django.contrib.auth import authenticate, login, logout
from .mixins import LogoutRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from . import forms


# Render LoginView(Form)
class LoginView(LogoutRequiredMixin, FormView):
    template_name = 'account/login.html'
    form_class = forms.LoginForm
    success_url = reverse_lazy('main:index')

    def form_valid(self, form):
        cleaned_data = form.cleaned_data

        # Get user and authenticate it
        user = authenticate(username=cleaned_data.get('username'), password=cleaned_data.get('password'))
        login(self.request, user=user)  # Login user

        return super().form_valid(form)


# Render LogoutView(func)
def logout_view(request):
    if request.user.is_authenticated:
        logout(request)

    return redirect('main:index')
