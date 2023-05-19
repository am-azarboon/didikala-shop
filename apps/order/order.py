from apps.product.models import Product, ProductCustom
from apps.cart.models import Cart, CartItem
from .models import Order, OrderItem


ORDER_SESSION_ID = 'order'


# SessionOrder Handler
class SessionOrder:
    def __init__(self, request):
        self.session = request.session
        order = self.session.get(ORDER_SESSION_ID)  # Get user order from sessions

        # Create order in session if not exists
        if not order:
            order = self.session[ORDER_SESSION_ID] = {}

        self.order = order  # Set user order

    def modify(self, key, value):
        self.order[key] = value  # Add new value
        self.save()

    def create_order(self):
        pass

    def save(self):
        self.session.modified = True  # Set session modified as True to allow changes
