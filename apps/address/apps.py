from django import gettext_lazy as _
from django import AppConfig


class AddressConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.address"
    verbose_name = _('Address Section')
