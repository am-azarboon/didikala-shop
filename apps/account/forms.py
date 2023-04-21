from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from .models import User, Profile
from django import forms


# UserCreation form
class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label=_('Password'), widget=forms.PasswordInput)
    password2 = forms.CharField(label=_('Password repeat'), widget=forms.PasswordInput)
    mobile = forms.CharField(label=_('Mobile number'), max_length=11)

    class Meta:
        model = User
        fields = ('mobile',)

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise ValidationError(_('Passwords are not match!'))
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])

        if commit:
            user.save()
        return user


# UserChange form
class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin
    disabled password hash display field.
    """
    password = ReadOnlyPasswordHashField(label=_('Password'))

    class Meta:
        model = User
        fields = ('email', 'password', 'mobile', 'access_level', 'is_active', 'is_admin')
