from django.contrib.auth.models import AbstractBaseUser
from django.utils.translation import gettext_lazy as _
from .managers import UserManager
from django.db import models


# ReCreate user model
class User(AbstractBaseUser):
    email = models.EmailField(_('Email Address'), max_length=255, null=True, blank=True)
    mobile = models.CharField(_('Mobile Number'), max_length=11, null=False, unique=True)
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
