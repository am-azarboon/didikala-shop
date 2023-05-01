from django.views.generic import View, TemplateView
from django.shortcuts import redirect
from django.urls import reverse
from .cart import Cart


# Render CartView
class CartView(TemplateView):
    template_name = 'cart/cart.html'
    content_type = 'text/html'

    def dispatch(self, request, *args, **kwargs):
        cart = Cart(request)

        # Redirect user to emtpy cart view if its cart is emtpy
        if cart.cart == {}:
            return redirect('cart:emtpy')

        return super(CartView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = Cart(self.request)  # Get or create user cart
        context['cart'] = cart  # Send cart as context to template
        context['price'] = cart.total_price()  # Get the total_price for all products

        return context


# Render CartEmptyView
class CartEmptyView(TemplateView):
    template_name = 'cart/cart_empty.html'
    content_type = 'text/html'

    def dispatch(self, request, *args, **kwargs):
        cart = Cart(request)

        # Redirect user to cart view if its cart is not empty
        if cart.cart != {}:
            return redirect('cart:cart')

        return super(CartEmptyView, self).dispatch(request, *args, **kwargs)


# Render CartAddView
class CartAddView(View):
    def get(self, request, pk):
        cart = Cart(request=request)  # Create or get user cart
        cart.cart_add(idkc=pk)  # Add new product to cart

        return redirect(reverse('product:detail', args=[pk]))  # Redirect to current product page

    def post(self, request):
        pass


# Render cart_remove_view
def cart_remove_view(request, pk):
    cart = Cart(request=request)  # Get user cart
    cart.cart_remove(idkc=str(pk))  # Remove product from cart

    return redirect('cart:cart')
