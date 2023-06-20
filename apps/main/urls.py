from django import path
from . import views

# urlpatterns' name
app_name = 'main'

# UrlPatterns
urlpatterns = [
    path('', views.IndexTemplateView.as_view(), name='index'),
]
