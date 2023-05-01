from apps.product.models import ProductCustom
from django.shortcuts import redirect


CART_SESSION_ID = 'cart'  # Save 'cart' in variable


class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(CART_SESSION_ID)  # Get user cart from sessions

        # Check if 'cart' is not exists
        if not cart:
            cart = self.session[CART_SESSION_ID] = {}

        self.cart = cart  # Set current user cart

    def __iter__(self):
        cart = self.cart.copy()

        for item in cart.values():
            product = ProductCustom.objects.get(idkc=item['idkc'])  # Get current product with idkc

            item['product'] = product
            item['total_price'] = int(product.selling_price * item['quantity'])  # Save total price
            yield item

    def total_price(self):
        cart = self.cart.copy()
        total_price = 0

        for item in cart.values():
            product = ProductCustom.objects.get(idkc=item['idkc'])  # Get each product
            price = int(product.selling_price * item['quantity'])  # Save item price(for all quantities)
            total_price += price

        return total_price

    def cart_add(self, idkc, quantity=1):
        product = ProductCustom.objects.get(idkc=idkc)  # Get current product

        # Add new product to cart
        if idkc not in self.cart:
            self.cart[idkc] = {
                'idk': product.product.idk,
                'idkc': product.idkc,
                'quantity': 0,
            }

        self.cart[idkc]['quantity'] += int(quantity)  # Add extra quantity
        self.save()

    def cart_remove(self, idkc):
        if idkc in self.cart:
            del self.cart[idkc]  # Del item if exists

        self.save()  # Save it

    def save(self):
        self.session.modified = True  # Set session modified as True to allow changes
