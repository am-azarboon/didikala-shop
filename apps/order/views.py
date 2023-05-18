from django.views.generic import View, TemplateView
from .mixins import NewLoginRequiredMixin
from apps.address.models import Address
from django.shortcuts import redirect
from apps.cart.cart import ModelCart
from .models import Order, OrderItem


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

    def get_context_data(self, *args, **kwargs):
        contexts = super().get_context_data(**kwargs)

        contexts['cart'] = ModelCart(self.request)  # Send user ModelCart as context

        try:  # Try to get active_address
            active_address = Address.objects.get(user=self.request.user, active=True)
            contexts['active_address'] = active_address  # Send User active_address as context
        except Address.DoesNotExist:
            contexts['active_address'] = None

        addresses = Address.objects.filter(user=self.request.user)
        contexts['addresses'] = addresses  # Send User addresses as context

        return contexts
