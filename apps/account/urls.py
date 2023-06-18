from django.urls import path
from . import views


# Urlpatterns' name
app_name = "account"

urlpatterns = [
    path('login', views.LoginView.as_view(), name="login"),
    path('register', views.RegisterView.as_view(), name="register"),
    path('mobile', views.MobileView.as_view(), name="mobile"),
    path('otp-check', views.OtpCheckView.as_view(), name="otp_check"),
    path('otp-send', views.otp_send_view, name="otp_send"),
    path('logout', views.logout_view, name="logout"),
]
