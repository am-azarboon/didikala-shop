from django import DetailView
from apps.cart.cart import SessionCart, ModelCart
from .models import ProductCustom
from apps.cart.models import CartItem


# Render ProductDetailView
class ProductDetailView(DetailView):
    model = ProductCustom
    template_name = 'product/product_detail.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super(ProductDetailView, self).get_context_data(**kwargs)
        context['in_cart'] = False

        # Check if user authenticated
        if self.request.user.is_authenticated:
            cart = ModelCart(self.request)

            # Check if product is in ModelCart
            if CartItem.objects.filter(product__idkc=self.kwargs.get('pk'), cart=cart.cart).exists():
                context['in_cart'] = True
        else:
            cart = SessionCart(self.request)  # Get the user cart from sessions

            # Send the added True to template if product is in SessionCart
            if str(self.kwargs.get('pk')) in cart.cart:
                context['in_cart'] = True

        return context
