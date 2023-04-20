from django.contrib.auth.base_user import BaseUserManager


# ReCreate UserManger model
class UserManager(BaseUserManager):
    def create_user(self, password=None, mobile=None, commit=False):
        """
        Creates and saves a User with the given data.
        """

        user = self.model(
            mobile=mobile,
            password=password
        )

        user.set_password(password)

        if commit:
            user.save(using=self._db)

        return user

    def create_superuser(self, mobile, password=None):
        """
        Creates and saves a superuser with the given data.
        """
        if mobile:
            user = self.create_user(mobile=mobile, password=password, commit=True)
        else:
            raise ValueError('Users must have a mobile number!')

        user.is_admin = True
        user.save(using=self._db)
        return user
