from django import gettext_lazy as _
from .validators import arithmetic_numbers
from apps.account.models import User
from django import models


# Province model
class Province(models.Model):
    id = models.BigIntegerField(_('ID'), primary_key=True, editable=False)
    name = models.CharField(_('Title'), max_length=32, default='')
    slug = models.SlugField(_('Slug'), max_length=64, allow_unicode=True, default='None')

    class Meta:
        verbose_name = _('Province')
        verbose_name_plural = _('Provinces')

    def __str__(self):
        return self.name


# City model
class City(models.Model):
    id = models.BigIntegerField(_('ID'), primary_key=True, editable=False)
    province = models.ForeignKey(Province, verbose_name=_('Province'), on_delete=models.CASCADE)
    name = models.CharField(_('Title'), max_length=32, default='')
    slug = models.SlugField(_('Slug'), max_length=64, allow_unicode=True, default='None')

    class Meta:
        verbose_name = _('City')
        verbose_name_plural = _('Cities')

    def __str__(self):
        return self.name


# UserAddress model
class Address(models.Model):
    user = models.ForeignKey(User, verbose_name=_('User'), on_delete=models.CASCADE, related_name='address')
    fullname = models.CharField(_('Full name'), max_length=32, default='')
    mobile = models.CharField(_('Mobile number'), max_length=11)
    province = models.ForeignKey(Province, verbose_name=_('Province'), max_length=32, null=True, on_delete=models.SET_NULL)
    city = models.ForeignKey(City, verbose_name=_('City'), max_length=32, null=True, on_delete=models.SET_NULL)
    address = models.TextField(_('Address'), max_length=256)
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
                item.save()

        return super(Address, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.user} - {self.address}"
