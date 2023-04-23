from django.contrib.auth.forms import ReadOnlyPasswordHashField
from .validators import mobile_format_check, email_format_check
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate
from .validators import arithmetic_numbers
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


# Login Form
class LoginForm(forms.Form):
    username = forms.CharField(max_length=128, required=True, widget=forms.TextInput(attrs={'class': 'input-ui pr-2', 'placeholder': _('Enter your mobile or email address')}))
    password = forms.CharField(max_length=128, required=True, widget=forms.PasswordInput(attrs={'class': 'input-ui pr-2', 'placeholder': _('Enter your password')}))

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        # Checking username format(email or mobile)
        if not mobile_format_check(username) and not email_format_check(username):
            raise ValidationError(_('Please Enter a valid mobile or email address'), code='INVALID-USERNAME')

        # Checking user existence
        user = authenticate(username=username, password=password)
        if user is None:
            raise ValidationError(_('Username or password is not correct'), code='USER-NOT-FOUND')

        return self.cleaned_data


# Register Form
class RegisterForm(forms.Form):
    mobile = forms.CharField(max_length=11, required=True, widget=forms.TextInput(attrs={'class': 'input-ui pr-2', 'placeholder': _('Enter your mobile number')}))
    password1 = forms.CharField(max_length=128, required=True, widget=forms.PasswordInput(attrs={'class': 'input-ui pr-2', 'placeholder': _('Enter password')}))
    password2 = forms.CharField(max_length=128, required=True, widget=forms.PasswordInput(attrs={'class': 'input-ui pr-2', 'placeholder': _('Repeat password')}))
    checkbox = forms.BooleanField(required=True, widget=forms.CheckboxInput(attrs={'class': 'custom-control-input'}))

    def clean(self):
        mobile = self.cleaned_data.get('mobile')
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        # Checking mobile format
        if not mobile_format_check(mobile):
            raise ValidationError(_('Enter a valid mobile number'), code='INVALID-MOBILE')

        # Checking passwords
        if password1 != password2:
            raise ValidationError(_('Passwords are not match'), code='PASSWORDS-MATCHING')

        # Checking user existence
        if User.objects.filter(mobile=mobile).exists():
            raise ValidationError(_('User with this mobile number is already exists'), code='USER-EXISTS')

        return self.cleaned_data
