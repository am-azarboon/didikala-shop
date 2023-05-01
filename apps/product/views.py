from django.utils.translation import gettext_lazy as _
from django.views.generic import DetailView, ListView
from django.shortcuts import redirect, reverse
from .models import Product, ProductCustom
from apps.cart.cart import Cart


# Render ProductDetailView
class ProductDetailView(DetailView):
    model = ProductCustom
    template_name = 'product/product_detail.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super(ProductDetailView, self).get_context_data(**kwargs)
        cart = Cart(self.request)  # Get the user cart from session

        # Send the added True to template if in item is in cart
        if str(self.kwargs.get('pk')) in cart.cart:
            context['added'] = True
        else:
            context['added'] = False  # Else send as false

        return context
