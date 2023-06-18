from .validators import mobile_format_check, email_format_check, arithmetic_numbers
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate
from .models import User
from django import forms


# UserCreation form
class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label=_("Password"), widget=forms.PasswordInput)
    password2 = forms.CharField(label=_("Password repeat"), widget=forms.PasswordInput)
    mobile = forms.CharField(label=_("Mobile number"), max_length=11)

    class Meta:
        model = User
        fields = ("mobile",)

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise ValidationError(_("Passwords are not match!"))
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.verified = True

        if commit:
            user.save()

        return user


# UserChange form
class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin
    disabled password hash display field.
    """
    password = ReadOnlyPasswordHashField(label=_("Password"))

    class Meta:
        model = User
        fields = ("email", "password", "mobile", "access_level", "is_active", "is_admin")


# Login form
class LoginForm(forms.Form):
    username = forms.CharField(max_length=128, required=True, widget=forms.TextInput(attrs={"class": "input-ui pr-2", "placeholder": _("Enter your mobile or email address")}))
    password = forms.CharField(max_length=128, required=True, widget=forms.PasswordInput(attrs={"class": "input-ui pr-2", "placeholder": _("Enter your password")}))

    def clean(self):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")

        # Checking username format(email or mobile)
        if not mobile_format_check(username) and not email_format_check(username):
            raise ValidationError(_("Mobile or email address is not valid"), code="INVALID-USERNAME")

        # Checking user existence
        user = authenticate(username=username, password=password)
        if user is None or not user.verified:
            raise ValidationError(_("Username or password is not correct"), code="USER-NOT-FOUND")

        return user


# Register form
class RegisterForm(forms.Form):
    mobile = forms.CharField(max_length=11, required=True, widget=forms.TextInput(attrs={"class": "input-ui pr-2", "placeholder": _("Enter your mobile number")}))
    password1 = forms.CharField(max_length=128, required=True, widget=forms.PasswordInput(attrs={"class": "input-ui pr-2", "placeholder": _("Enter password")}))
    password2 = forms.CharField(max_length=128, required=True, widget=forms.PasswordInput(attrs={"class": "input-ui pr-2", "placeholder": _("Repeat password")}))
    checkbox = forms.BooleanField(required=True, widget=forms.CheckboxInput(attrs={"class": "custom-control-input"}))

    def clean(self):
        mobile = self.cleaned_data.get("mobile")
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        # Checking mobile format
        if not mobile_format_check(mobile):
            raise ValidationError(_("Mobile number is not valid"), code="INVALID-MOBILE")

        # Checking passwords
        if password1 != password2:
            raise ValidationError(_("Passwords are not match"), code="PASSWORDS-MATCHING")

        # Checking user existence
        if User.objects.filter(mobile=mobile, verified=True).exists():
            raise ValidationError(_("User with this mobile number is already exists"), code="USER-EXISTS")

        return self.cleaned_data


# Mobile form
class MobileForm(forms.Form):
    mobile = forms.CharField(max_length=11, required=True, widget=forms.TextInput(attrs={"class": "input-ui pr-2", "placeholder": _("Enter your mobile number")}))

    def clean(self):
        mobile = self.cleaned_data.get("mobile")

        # Check mobile validation
        if not mobile_format_check(mobile):
            raise ValidationError(_("Mobile number is not valid"), code="INVALID-MOBILE")

        # Check user existence
        if not User.objects.filter(mobile=mobile, verified=True).exists():
            raise ValidationError(_("User with this mobile number is not exists"), code="USER-NOT-FOUND")

        return self.cleaned_data


# OtpCheck form
class OtpCheckForm(forms.Form):
    number_one = forms.CharField(max_length=1, required=True, validators=[arithmetic_numbers], widget=forms.TextInput(attrs={"class": "line-number"}))
    number_two = forms.CharField(max_length=1, required=True, validators=[arithmetic_numbers], widget=forms.TextInput(attrs={"class": "line-number"}))
    number_three = forms.CharField(max_length=1, required=True, validators=[arithmetic_numbers], widget=forms.TextInput(attrs={"class": "line-number"}))
    number_four = forms.CharField(max_length=1, required=True, validators=[arithmetic_numbers], widget=forms.TextInput(attrs={"class": "line-number"}))
    number_five = forms.CharField(max_length=1, required=True, validators=[arithmetic_numbers], widget=forms.TextInput(attrs={"class": "line-number"}))

    def clean(self):
        cleaned_data = self.cleaned_data

        # Concatenate numbers
        otp_code = cleaned_data["number_one"] + cleaned_data["number_two"] + cleaned_data["number_three"] + \
            cleaned_data["number_four"] + cleaned_data["number_five"]

        return otp_code
