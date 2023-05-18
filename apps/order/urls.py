from django.urls import path
from . import views


# urlpatterns' name
app_name = 'order'

urlpatterns = [
    path('shopping', views.ShoppingView.as_view(), name='shopping'),
]
