from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError


# Number Only validator
def positive_number_valid(value):
    for num in value:
        global flag
        flag = False

        for i in range(0, 10):
            if num == str(i):
                flag = True
                break

        if flag is False:
            raise ValidationError(_('Invalid melli code'), code='invalid_melli_code')
