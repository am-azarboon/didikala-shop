from django.urls import path
from . import views


# urlpatterns' name
app_name = 'order'

urlpatterns = [
    path('info', views.ShoppingView.as_view(), name='shopping'),
    path('payment', views.PaymentView.as_view(), name='payment'),
]
