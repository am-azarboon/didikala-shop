from .models import Address, Province, City
from django import forms


# AddressForm
class AddressForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AddressForm, self).__init__(*args, **kwargs)
        self.fields['author'].choices = list(Province.objects.values_list('id', 'name'))

        self.fields['books'].choices = list(City.objects.values_list('id', 'name'))

    class Meta:
        model = Address
        exclude = ('user', 'created_at', 'updated_at')
