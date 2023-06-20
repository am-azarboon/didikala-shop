from .validators import mobile_format_check, arithmetic_numbers
from django import gettext_lazy as _
from django import ValidationError
from .models import Address, City
from django import forms


# AddressForm
class AddressForm(forms.ModelForm):

    class Meta:
        model = Address
        exclude = ('user', 'active', 'created_at', 'updated_at')

        widgets = {
            'fullname': forms.TextInput(attrs={'class': 'input-ui pr-2 text-right', 'placeholder': _('Enter your name')}),
            'mobile': forms.TextInput(attrs={'class': 'input-ui pl-2 dir-ltr text-left', 'placeholder': '09xxxxxxxxx', 'maxlentgh': 11}),
            'province': forms.Select(attrs={'class': 'input-ui custom-select-ui'}),
            'city': forms.Select(attrs={'class': 'input-ui custom-select-ui'}),
            'address': forms.Textarea(attrs={'class': 'input-ui pr-2 text-right', 'placeholder': _('Please enter your address')}),
            'post_code': forms.TextInput(attrs={'class': 'input-ui pl-2 dir-ltr text-left placeholder-right', 'placeholder': _('Please enter your post code without dash or comma')})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['city'].queryset = City.objects.none()

        if 'province' in self.data:
            try:
                province_id = int(self.data.get('province'))
                self.fields['city'].queryset = City.objects.filter(province_id=province_id).order_by('name')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            self.fields['city'].queryset = self.instance.province.city_set.order_by('name')
