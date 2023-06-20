from django import path
from . import views


# urlpatterns' name
app_name = 'address'

urlpatterns = [
    path('add', views.AddAddressView.as_view(), name='add'),
    path('delete/<int:pk>', views.DeleteAddressView.as_view(), name='delete'),
    path('active/<int:pk>', views.active_address_view, name='active'),
    path('cities', views.get_cities, name='get_cities'),  # Ajax
]
