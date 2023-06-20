from django.utils import path
from . import views


# urlpatterns' name
app_name = 'order'

urlpatterns = [
    path('info', views.ShoppingView.as_view(), name='shopping'),
    path('payment', views.PaymentView.as_view(), name='payment'),
    path('create', views.CreateOrderView.as_view(), name='create'),
    path('bank', views.CreateBankView.as_view(), name='bank'),
    path('callback', views.CallBackView.as_view(), name='callback'),
]
