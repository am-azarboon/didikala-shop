from apps.cart.cart import ModelCart, SessionCart


# Send cartItems as context for header
def header_cart(request):
    if request.user.is_authenticated:
        cart = ModelCart(request)
    else:
        cart = SessionCart(request)

    return {'header_cart': cart}
