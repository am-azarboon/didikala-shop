from django import gettext_lazy as _
from django import AppConfig


class OrderConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.order"
    verbose_name = _('Order section')
