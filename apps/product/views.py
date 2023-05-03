from django.utils.translation import gettext_lazy as _
from django.views.generic import DetailView, ListView
from apps.cart.cart import SessionCart, ModelCart
from django.shortcuts import redirect, reverse
from .models import Product, ProductCustom
from apps.cart.models import CartItem


# Render ProductDetailView
class ProductDetailView(DetailView):
    model = ProductCustom
    template_name = 'product/product_detail.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super(ProductDetailView, self).get_context_data(**kwargs)
        context['added'] = False

        if self.request.user.is_authenticated:
            cart = ModelCart(self.request)
            print('outside cart file : ', cart.cart)

            if CartItem.objects.filter(product__idkc=self.kwargs.get('pk'), cart=cart.cart).exists():
                context['added'] = True
                return context

        cart = SessionCart(self.request)  # Get the user cart from sessions

        # Send the added True to template if in item is in cart
        if str(self.kwargs.get('pk')) in cart.cart:
            context['added'] = True

        return context
