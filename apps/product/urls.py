from django.utils import path
from . import views

# urlpatterns' name
app_name = 'product'

urlpatterns = [
    path('detail/<int:pk>', views.ProductDetailView.as_view(), name='detail'),
]
