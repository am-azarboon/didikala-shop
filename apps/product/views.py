from django.utils.translation import gettext_lazy as _
from django.views.generic import DetailView, ListView
from django.shortcuts import redirect, reverse
from .models import Product, ProductCustom
from django.shortcuts import render


# Render ProductDetailView
class ProductDetailView(DetailView):
    model = ProductCustom
    template_name = 'product/product_detail.html'
    context_object_name = 'product'
