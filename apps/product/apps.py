from django.utils.translation import gettext_lazy as _
from django.apps import AppConfig


class ProductConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.product"
    verbose_name = _('Products Section')

    def ready(self):
        import apps.product.signals
