from .enums import OrderStatus, DeliveryType, PaymentMethod
from django.utils.translation import gettext_lazy as _
from apps.product.models import ProductCustom
from apps.account.models import User
from django.db import models


# Order Model
class Order(models.Model):
    PaymentMethod = PaymentMethod
    DeliveryType = DeliveryType
    Status = OrderStatus

    user = models.ForeignKey(User, verbose_name=_('User'), on_delete=models.DO_NOTHING, related_name='order')
    quantity = models.PositiveIntegerField(_('Quantity'), default=0)
    payable_price = models.IntegerField(_('Payable price'), default=0)
    discount_price = models.IntegerField(_('Discount price'), default=0)
    address_info = models.TextField(_('Address info'), max_length=256, default='')
    delivery_type = models.CharField(_('Delivery type'), max_length=32, choices=DeliveryType.choices, default=DeliveryType.choices[0])
    payment_method = models.CharField(_('Payment method'), max_length=32, choices=PaymentMethod.choices, default=DeliveryType.choices[0])
    status = models.CharField(_('Status'), max_length=32, choices=Status.choices, default=Status.choices[0])
    is_paid = models.BooleanField(_('Is success'), default=False)

    created_at = models.DateTimeField(_('Create time'), auto_now_add=True)

    class Meta:
        verbose_name = _('Order')
        verbose_name_plural = _('Orders')
        ordering = ['-created_at']


# OrderItem model
class OrderItem(models.Model):
    order = models.ForeignKey(Order, verbose_name=_('Order'), on_delete=models.CASCADE, related_name='order_item')
    product = models.ForeignKey(ProductCustom, verbose_name=_('Product'), on_delete=models.DO_NOTHING, related_name='order_item')
    quantity = models.PositiveIntegerField(_('Quantity purchased'), default=0)
    total_price = models.IntegerField(_('Total price'), default=0)

    class Meta:
        verbose_name = _('Order item')
        verbose_name_plural = _('Order items')
