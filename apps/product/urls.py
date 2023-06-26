from django.urls import path, re_path
from . import views


# urlpatterns' name
app_name = "product"

urlpatterns = [
    path('<int:pk>', views.ProductDetailView.as_view(), name="detail"),
    path('main/<slug:slug>', views.CategoryMainView.as_view(), name="category_main"),
    path('search/category-<slug:slug>', views.CategorySearchView.as_view(), name="category_search"),
    # re_path(r'^search/category-(?P<slug>[\w-]+)/$', views.CategorySearch.as_view(), name='category_search'),
    path('menu', views.NavbarMenuView.as_view(), name="navbar_menu"),
]
