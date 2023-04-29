from django.urls import path
from . import views

# urlpatterns' name
app_name = 'cart'

urlpatterns = [
    path('', views.CartView.as_view(), name='cart'),
    path('emtpy', views.CartEmptyView.as_view(), name='emtpy'),
]
