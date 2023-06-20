from django.contrib.auth.models import BaseUserManager
from django.utils.translation import gettext_lazy as _
from .enums import UserAccessLevel


# ReCreate UserManger model
class UserManager(BaseUserManager):
    def create_user(self, password=None, mobile=None, verify=False):
        """ Creates and saves a User with the given data. """

        user = self.model(mobile=mobile, password=password)
        user.set_password(password)
        user.verified = verify

        user.save(using=self._db)

        return user

    def create_superuser(self, mobile, password=None):
        """
        Creates and saves a superuser with the given data.
        """
        if mobile:
            user = self.create_user(mobile=mobile, password=password, verify=True)
        else:
            raise ValueError(_("Users must have a mobile number!"))

        user.is_admin = True  # Set the admin 'True'
        user.access_level = UserAccessLevel.MANAGER  # Set the access_level to 'Manager'

        user.save(using=self._db)

        return user
