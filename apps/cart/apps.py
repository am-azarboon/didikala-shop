from django.utils.translation import gettext_lazy as _
from django.apps import AppConfig


class CartConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.cart"
    verbose_name = _('Cart Section')
