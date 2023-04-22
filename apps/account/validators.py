from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
import random
import re


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


# Check mobile number format(Iran)
def mobile_format_check(string):
    mobile_regex = "^09(1[0-9]|3[1-9]|2[1-9])-?[0-9]{3}-?[0-9]{4}$"
    if re.search(mobile_regex, string):
        return True
    return False


# Check email format
def email_format_check(string):
    try:
        validate_email(string)
        return True
    except ValidationError:
        return False
