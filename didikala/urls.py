from django.conf.urls.static import static
from django.urls import path, include
from django.contrib import admin
import settings


urlpatterns = [
    path("admin/", admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
