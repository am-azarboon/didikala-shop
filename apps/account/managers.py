from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _
from .enums import UserAccessLevel


# ReCreate UserManger model
class UserManager(BaseUserManager):
    def create_user(self, password=None, mobile=None):
        """ Creates and saves a User with the given data. """

        user = self.model(
            mobile=mobile,
            password=password
        )

        user.set_password(password)

        user.save(using=self._db)

        return user

    def create_superuser(self, mobile, password=None):
        """
        Creates and saves a superuser with the given data.
        """
        if mobile:
            user = self.create_user(mobile=mobile, password=password)
        else:
            raise ValueError(_("Users must have a mobile number!"))

        user.is_admin = True  # Set the admin 'True'
        user.verified = True  # Set the verified 'True'
        user.access_level = UserAccessLevel.choices[1]  # Set the access_level to 'Manager'

        user.save(using=self._db)

        return user
