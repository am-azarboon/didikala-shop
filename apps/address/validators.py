from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError


# Arithmetic numbers only
def arithmetic_numbers(value):
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    for num in value:
        if num not in numbers:
            error = _('Invalid input')
            raise ValidationError(error, code='invalid_melli_code')
