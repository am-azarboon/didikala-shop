from django.utils.translation import gettext_lazy as _
from django.conf.urls.static import static
from django.urls import path, include
from django.contrib import admin
from . import settings


admin.site.site_header = _('Shop Management')
admin.site.site_title = _('Shop Management')
admin.site.index_title = _('Admin Panel')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/', include('apps.account.urls', namespace='account')),
    path('address/', include('apps.address.urls', namespace='address')),
    path('product/', include('apps.product.urls', namespace='product')),
    path('cart/', include('apps.cart.urls', namespace='cart')),
    path('order/', include('apps.order.urls', namespace='order')),
    path('', include('apps.main.urls', namespace='main')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# handling the 404 error
handler404 = 'apps.main.views.error_404_view'
