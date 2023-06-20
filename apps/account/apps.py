from django import gettext_lazy as _
from django import AppConfig


class AccountConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.account"
    verbose_name = _('Accounts Section')

    def ready(self):
        pass
