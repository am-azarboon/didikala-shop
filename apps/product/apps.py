from django import gettext_lazy as _
from django import AppConfig


class ProductConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.product"
    verbose_name = _('Products Section')

    def ready(self):
        pass
