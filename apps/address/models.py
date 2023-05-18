from django.utils.translation import gettext_lazy as _
from .validators import arithmetic_numbers
from apps.account.models import User
from django.db import models


# Province model
class Province(models.Model):
    id = models.CharField(_('ID'), primary_key=True, max_length=2, validators=[arithmetic_numbers])
    slug = models.SlugField(_('Slug'), max_length=32, default='None')
    name = models.CharField(_('Title fa'), max_length=32, default='')

    class Meta:
        verbose_name = _('Province')
        verbose_name_plural = _('Provinces')

    def __str__(self):
        return self.name


# City model
class City(models.Model):
    province = models.ForeignKey(Province, verbose_name=_('Province'), on_delete=models.CASCADE)
    slug = models.SlugField(_('Slug'), max_length=32, default='None')
    name = models.CharField(_('Title fa'), max_length=32, default='')

    class Meta:
        verbose_name = _('City')
        verbose_name_plural = _('Cities')

    def __str__(self):
        return self.name


# UserAddress model
class Address(models.Model):
    user = models.ForeignKey(User, verbose_name=_('User'), on_delete=models.CASCADE, related_name='address')
    firstname = models.CharField(_('First name'), max_length=32, default='')
    lastname = models.CharField(_('Last name'), max_length=32, default='')
    mobile = models.CharField(_('Mobile number'), max_length=11, default='09000000000')
    province = models.CharField(_('Province'), max_length=32, default='None')
    city = models.CharField(_('City'), max_length=32, default='None')
    address = models.TextField(_('Address'), max_length=256, unique=True)
    post_code = models.CharField(_('Postal_code'), max_length=10, unique=True, validators=[arithmetic_numbers])
    active = models.BooleanField(_('Active'), default=False)

    # Create/update time
    created_at = models.DateTimeField(_('Create time'), auto_now_add=True, null=True)
    updated_at = models.DateTimeField(_('Update time'), auto_now=True, null=True)

    class Meta:
        verbose_name = _('User address')
        verbose_name_plural = _('User addresses')

    def save(self, *args, **kwargs):
        # DeActivate other addresses if an address activated new
        if self.active is True:
            for item in Address.objects.filter(user=self.user):
                item.active = False

        return super(Address, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.user} - {self.address}"
