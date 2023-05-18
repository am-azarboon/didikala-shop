from django.utils.translation import gettext_lazy as _
from django.db.models import TextChoices


# OrderStatus Choices
class OrderStatus(TextChoices):
    UNSUCCESSFUL = 'unsuccessful', _('Unsuccessful')
    SUCCESSFUL = 'successful', _('Successful')
    PENDING = 'pending', _('Pending')
    DISPATCHING = 'dispatching', _('Dispatching')
    DISPATCHED = 'dispatched', _('Dispatched')
