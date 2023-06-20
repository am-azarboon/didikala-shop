from django import View, TemplateView
from .cart import SessionCart, ModelCart
from django import redirect
from django import reverse
from django import Http404


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
        contexts = super().get_context_data(**kwargs)

        if self.request.user.is_authenticated:
            cart = ModelCart(self.request)
        else:
            cart = SessionCart(self.request)  # Get or create user cart

        contexts['cart'] = cart  # Send cart as context to template
        return contexts


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


# Render item_add_view
def item_plus_view(request, pk, quantity):
    if request.user.is_authenticated:
        cart = ModelCart(request)
    else:
        cart = SessionCart(request)  # Create or get user cart

    # Check quantity range(0 or 1)
    if int(quantity) < 0 or int(quantity) > 1:
        raise Http404

    # Change the minus to -1
    if not int(quantity):
        quantity = -1

    cart.cart_add(idkc=pk, quantity=quantity)  # Add extra quantity to item

    return redirect('cart:cart')


# Render cart_remove_view
def cart_remove_view(request, pk):
    if request.user.is_authenticated:
        cart = ModelCart(request)  # Get user ModelCart
    else:
        cart = SessionCart(request)  # Get user SessionCart

    cart.cart_remove(idkc=str(pk))  # Remove product from cart

    return redirect('cart:cart')
