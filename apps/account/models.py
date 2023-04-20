from django.contrib.auth.models import AbstractBaseUser
from django.utils.translation import gettext_lazy as _
from .managers import UserManager
from django.db import models
from .enums import *


# ReCreate User model
class User(AbstractBaseUser):
    AccessLevel = UserAccessLevel

    # Model Fields
    email = models.EmailField(_('Email address'), max_length=255, null=True, blank=True)
    mobile = models.CharField(_('Mobile number'), max_length=11, null=False, unique=True)
    access_level = models.CharField(_('Access level'), max_length=32, choices=AccessLevel.choices, default=AccessLevel.choices[0])
    is_active = models.BooleanField(_('Active'), default=True)
    is_admin = models.BooleanField(_('Admin'), default=False)

    objects = UserManager()

    USERNAME_FIELD = 'mobile'

    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('User account')
        verbose_name_plural = _('Users accounts')

    def __str__(self):
        return self.mobile

    def has_perm(self, perm, obj=None):
        """Does the user have a specific permission?"""
        # Simplest possible answer: Yes, always
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
