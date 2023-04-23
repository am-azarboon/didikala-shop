from django.utils.translation import gettext_lazy as _
from django.db.models import TextChoices


# UserAccessLevel Choices
class UserAccessLevel(TextChoices):
    USER = 'user', _('User')
    MANAGER = 'manager', _('Manager')
    SELLER = 'seller', _('Seller')
    CREATOR = 'creator', _('Creator')


# UserGender Choices
class UserGender(TextChoices):
    MALE = 'm', _('Male')
    FEMALE = 'f', _('Female')
