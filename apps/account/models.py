from django.contrib.auth.models import AbstractBaseUser
from django.utils.translation import gettext_lazy as _
from django_jalali.db import models as jmodels
from .validators import arithmetic_numbers
from .managers import UserManager
from django.db import models
from .enums import *


# ReCreate User model
class User(AbstractBaseUser):
    AccessLevel = UserAccessLevel

    # Model Fields
    email = models.EmailField(_("Email address"), max_length=255, null=True, blank=True)
    mobile = models.CharField(_("Mobile number"), max_length=11, null=False, unique=True)
    is_active = models.BooleanField(_("Active"), default=True)
    is_admin = models.BooleanField(_("Admin"), default=False)
    verified = models.BooleanField(_("Verified"), editable=False, default=False)
    access_level = models.CharField(_("Access level"), max_length=32, choices=AccessLevel.choices, default=AccessLevel.choices[0])

    objects = UserManager()  # Set UserManager as model object manager

    USERNAME_FIELD = "mobile"

    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _("User account")
        verbose_name_plural = _("Users accounts")

        permissions = [
            ("is_manager", _("Is_manager")),
            ("is_seller", _("Is_seller")),
            ("is_creator", _("Is_creator")),
        ]

    def __str__(self):
        return self.mobile

    def has_perm(self, perm, obj=None):
        """Does the user have a specific permission?"""
        # Check access_level permission
        if perm == "is_user" and self.access_level != self.AccessLevel.USER:
            return False
        elif perm == "is_manager" and self.access_level != self.AccessLevel.MANAGER:
            return False
        elif perm == "is_seller" and self.access_level != self.AccessLevel.SELLER:
            return False
        elif perm == "is_creator" and self.access_level != self.AccessLevel.CREATOR:
            return False

        return True

    def has_module_perms(self, app_label):
        """Does the user have permissions to view the app `app_label`?"""
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        """Is the user a member of staff?"""
        # Simplest possible answer: All admins are staff
        return self.is_admin


# UserProfile model
class Profile(models.Model):
    Gender = UserGender

    user = models.OneToOneField(User, verbose_name=_("User"), on_delete=models.CASCADE)
    firstname = models.CharField(_("First name"), max_length=64, null=True, blank=True)
    lastname = models.CharField(_("Last name"), max_length=64, null=True, blank=True)
    gender = models.CharField(_("Gender"), max_length=8, null=True, blank=True, choices=Gender.choices)
    melli_code = models.CharField(_("Melli code"), max_length=10, null=True, blank=True, validators=[arithmetic_numbers])

    # Confirmation info
    is_foreign_citizen = models.BooleanField(_("I\'m foreign citizen"), default=False)
    is_subscriber = models.BooleanField(_("Subscribe"), default=False)

    # Additional info
    date_of_birth = jmodels.jDateField(_("Date of birth"), null=True, blank=True)
    profile_image = models.ImageField(_("Profile image"), null=True, blank=True, upload_to="image/profiles")

    # Create/update time
    created_at = models.DateTimeField(_("Created time"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated time"), auto_now=True)

    class Meta:
        verbose_name = _("User profile")
        verbose_name_plural = _("Users profiles")

    def __str__(self):
        return self.user.mobile


# One time passwords model
class Otp(models.Model):
    token = models.CharField(_("Token"), max_length=128, null=True)
    mobile = models.CharField(_("Mobile"), max_length=11, unique=True)
    otp = models.CharField(_("One time password"), max_length=5, null=True)
    created_at = models.DateTimeField(_("Create time"), auto_now_add=True, editable=True)

    class Meta:
        verbose_name = "One time password"
        verbose_name_plural = "One time passwords"

    def __str__(self):
        return f"{self.mobile} - {self.token}"
