from django.urls import path
from . import views


# urlpatterns' name
app_name = "product"

urlpatterns = [
    path('<int:pk>', views.ProductDetailView.as_view(), name="detail"),
    path('menu', views.NavbarMenuView.as_view(), name="navbar_menu"),
]
