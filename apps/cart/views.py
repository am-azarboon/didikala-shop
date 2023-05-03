from django.views.generic import View, TemplateView
from .cart import SessionCart, ModelCart
from django.shortcuts import redirect
from django.urls import reverse


# Render CartView
class CartView(TemplateView):
    template_name = 'cart/cart.html'
    content_type = 'text/html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            cart = ModelCart(request)  # Get user ModelCart if user is authenticated
        else:
            cart = SessionCart(request)  # Get or create user shopping cart

        # Redirect user to emtpy cart view if its cart is emtpy
        if not cart.total_price():
            return redirect('cart:emtpy')

        return super(CartView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.user.is_authenticated:
            cart = ModelCart(self.request)
            context['cart'] = cart
        else:
            cart = SessionCart(self.request)  # Get or create user cart
            context['cart'] = cart  # Send cart as context to template

        return context


# Render CartEmptyView
class CartEmptyView(TemplateView):
    template_name = 'cart/cart_empty.html'
    content_type = 'text/html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            cart = ModelCart(request)  # Get or create user ModelCart
        else:
            cart = SessionCart(request)  # Get or create user SessionCart

        # Redirect user to cart view if its cart is not empty
        if cart.total_price():
            return redirect('cart:cart')

        return super(CartEmptyView, self).dispatch(request, *args, **kwargs)


# Render cart_add_view
def cart_add_view(request, pk):
    if request.user.is_authenticated:
        cart = ModelCart(request)
    else:
        cart = SessionCart(request)  # Create or get user cart

    cart.cart_add(idkc=pk, quantity=1)  # Add new product to cart

    return redirect(reverse('product:detail', args=[pk]))  # Redirect to current product page


# Render cart_remove_view
def cart_remove_view(request, pk):
    if request.user.is_authenticated:
        cart = ModelCart(request)  # Get user ModelCart
    else:
        cart = SessionCart(request)  # Get user SessionCart

    cart.cart_remove(idkc=str(pk))  # Remove product from cart

    return redirect('cart:cart')
