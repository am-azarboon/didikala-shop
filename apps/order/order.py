from django import IntegrityError, InternalError
from django import get_object_or_404
from apps.cart.models import CartItem, Cart
from apps.address.models import Address
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

    def create_order(self, request):
        order = self.order.copy()
        user = request.user  # Get user from request

        cart = get_object_or_404(Cart, user=user)
        cart_items = CartItem.objects.filter(cart__user=order['user'])  # Get user CartItems

        # Get user active address and create address info text
        address = get_object_or_404(Address, user=request.user, active=True)
        address_info = f"{address.province}-{address.city} --- {address.mobile} --- {address.address} -- {address.post_code}"

        # Calc total quantity and discount
        quantity = 0
        discount = 0
        for item in cart_items.all():
            quantity += int(item.quantity)
            discount += int(item.base_total_price - item.total_price)

        # Calc payable_price based on delivery type
        if order['delivery_type'] == 'N':
            payable_price = int(cart.total_price + 150000)
        else:
            payable_price = int(cart.total_price + 350000)

        # Create new order
        try:
            order = Order.objects.create(user=user, quantity=quantity, discount_price=discount, address_info=address_info,
                                         payable_price=payable_price, delivery_type=order['delivery_type'],
                                         payment_method=order['payment_method'],)

            order.oid = int(1000 + order.id)  # Create oid with base id
            order.save()

            self.modify(key='oid', value=str(order.oid))  # Save order oid in to sessions

        except (IntegrityError, InternalError):
            return False

        # Create order_items
        for item in cart_items.all():
            try:
                OrderItem.objects.create(order=order, product=item.product, quantity=item.quantity, total_price=item.total_price)
            except IntegrityError:
                return False

        return True

    def delete_order(self):
        try:
            del self.session[ORDER_SESSION_ID]
        except self.session.DoesNotExists:
            self.save()

    def save(self):
        self.session.modified = True  # Set session modified as True to allow changes
