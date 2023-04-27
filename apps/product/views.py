from django.utils.translation import gettext_lazy as _
from django.views.generic import DetailView, ListView
from django.shortcuts import redirect, reverse
from django.shortcuts import render


# Render ProductDetailView
class ProductDetailView(DetailView):
    model = ''
    template_name = 'product/product_detail.html'
    context_object_name = 'product'
