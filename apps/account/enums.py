from django.utils.translation import gettext_lazy as _
from django.db.models import TextChoices


# UserAccessLevel Choices
class UserAccessLevel(TextChoices):
    USER = 'user', _('User')
    SELLER = 'seller', _('Seller')
    MANAGER = 'manager', _('Manager')
    CREATOR = 'creator', _('Creator')


# UserGender Choices
class UserGender(TextChoices):
    MALE = 'm', _('Male')
    FEMALE = 'f', _('Female')
