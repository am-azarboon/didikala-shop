from django.utils.translation import gettext_lazy as _
from apps.product.models import ProductCustom
from apps.account.models import User
from django.db import models


# Cart model
class Cart(models.Model):
    user = models.OneToOneField(User, verbose_name=_('User'), on_delete=models.CASCADE, related_name='cart')
    total_price = models.IntegerField(_('Total price'), default=0, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Shopping cart')
        verbose_name_plural = _('Shopping Carts')


# CartItem model
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, verbose_name=_('Cart items'), on_delete=models.CASCADE, related_name='cart_item')
    product = models.ForeignKey(ProductCustom, verbose_name=_('Product'), on_delete=models.DO_NOTHING, related_name='cart_item')
    idkc = models.BigIntegerField(_('idkc'), default=0, editable=False)
    quantity = models.PositiveIntegerField(_('Quantity'), default=0)
    base_total_price = models.IntegerField(_('Base total price'), default=0, editable=False)
    total_price = models.IntegerField(_('Total price'), default=0, editable=False)

    class Meta:
        verbose_name = _('Cart item')
        verbose_name_plural = _('Cart items')
