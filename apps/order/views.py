from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView
from apps.address.forms import AddressForm
from .mixins import NewLoginRequiredMixin
from apps.address.models import Address
from django.shortcuts import redirect
from apps.cart.cart import ModelCart
from .order import SessionOrder


# Render ShoppingView
class ShoppingView(NewLoginRequiredMixin, TemplateView):
    template_name = 'order/shopping.html'
    content_type = 'text/html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            cart = ModelCart(request)  # Get or create user ModelCart
            if not cart.total_price():
                return redirect('cart:emtpy')  # Redirect user to empty cart if cart is empty

        return super(ShoppingView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        contexts = super().get_context_data(**kwargs)
        addresses = Address.objects.filter(user=self.request.user)

        contexts['cart'] = ModelCart(self.request)  # Send user ModelCart as context
        contexts['form'] = AddressForm()  # Send address form as context

        try:  # Try to get active_address
            active_address = addresses.get(active=True)
            contexts['active_address'] = active_address  # Send User active_address as context
        except (Address.DoesNotExist, Address.MultipleObjectsReturned):
            contexts['active_address'] = None

        contexts['addresses'] = addresses  # Send User addresses as context

        return contexts


# Render PaymentView
class PaymentView(TemplateView):
    template_name = 'order/payment.html'
    content_type = 'text/html'

    def post(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            delivery_type = self.request.POST.get('deliveryType')  # Get posted delivery type
            active_address = get_object_or_404(Address, user=self.request.user, active=True)  # Get user active address

            # Get user order from sessions and set new values
            order = SessionOrder(self.request)
            order.modify(key='user', value=self.request.user.id)
            order.modify(key='delivery_type', value=delivery_type)
            order.modify(key='address_info', value=active_address.id)
            order.modify(key='is_paid', value=False)

            print(order.order)
        return self.get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        contexts = super().get_context_data(**kwargs)
        order = SessionOrder(self.request)

        if order.order['delivery_type'] == 'N':
            contexts['delivery_type'] = 'N'
        else:
            contexts['delivery_type'] = 'Q'

        contexts['cart'] = ModelCart(self.request)  # Send user ModelCart as context

        return contexts
