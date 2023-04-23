from django.urls import path
from . import views

# Urlpatterns' name
app_name = 'account'

urlpatterns = [
    path('login', views.LoginView.as_view(), name='login'),
    path('logout', views.logout_view, name='logout'),
]
