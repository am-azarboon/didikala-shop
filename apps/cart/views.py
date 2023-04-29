from django.views.generic import View, TemplateView
from django.shortcuts import redirect


# Render CartView
class CartView(TemplateView):
    template_name = 'cart/cart.html'
    content_type = 'text/html'


# Render CartEmptyView
class CartEmptyView(TemplateView):
    template_name = 'cart/cart_empty.html'
    content_type = 'text/html'

