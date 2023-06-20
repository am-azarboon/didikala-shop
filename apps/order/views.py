from azbankgateways import bankfactories, models as bank_models, default_settings as settings
from azbankgateways.exceptions import AZBankGatewaysException
from django import HttpResponseNotFound, HttpResponse, Http404
from django import redirect, reverse, get_object_or_404
from django import LoginRequiredMixin
from django import TemplateView, View
from apps.product.models import ProductCustom
from apps.address.forms import AddressForm
from apps.address.models import Address
from apps.cart.cart import ModelCart
from .models import Order, OrderItem
from .order import SessionOrder


# Render ShoppingView
class ShoppingView(LoginRequiredMixin, TemplateView):
    template_name = 'order/shopping.html'
    content_type = 'text/html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            cart = ModelCart(request)  # Get or create user ModelCart
            if not cart.total_price():
                return redirect('cart:emtpy')  # Redirect user to empty cart if cart is empty

        return super(ShoppingView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        contexts = super().get_context_data(**kwargs)
        addresses = Address.objects.filter(user=self.request.user)

        contexts['cart'] = ModelCart(self.request)  # Send user ModelCart as context
        contexts['form'] = AddressForm()  # Send address form as context

        try:  # Try to get active_address
            active_address = addresses.get(active=True)
            contexts['active_address'] = active_address  # Send User active_address as context
        except (Address.DoesNotExist, Address.MultipleObjectsReturned):
            contexts['active_address'] = None

        contexts['addresses'] = addresses  # Send User addresses as context

        return contexts


# Render PaymentView
class PaymentView(LoginRequiredMixin, TemplateView):
    template_name = 'order/payment.html'
    content_type = 'text/html'

    def post(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            delivery_type = self.request.POST.get('deliveryType')  # Get posted delivery type

            try:
                active_address = Address.objects.get(user=self.request.user, active=True)  # Get user active address
            except Address.DoesNotExist:
                return redirect('order:shopping')

            # Get user order from sessions and set new values
            order = SessionOrder(self.request)
            order.modify(key='user', value=self.request.user.id)
            order.modify(key='delivery_type', value=delivery_type)
            order.modify(key='address_info', value=active_address.id)
            order.modify(key='is_paid', value=False)

        return self.get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        contexts = super().get_context_data(**kwargs)
        order = SessionOrder(self.request)

        if order.order['delivery_type'] == 'N':
            contexts['delivery_type'] = 'N'
        else:
            contexts['delivery_type'] = 'Q'

        contexts['cart'] = ModelCart(self.request)  # Send user ModelCart as context

        return contexts


# OrderCreateView
class CreateOrderView(LoginRequiredMixin, View):
    def post(self, request):
        payment_method = request.POST.get('paymentMethod')
        order = SessionOrder(request)  # Get user order from sessions
        order.modify(key='payment_method', value=str(payment_method))  # Set payment_method in order session

        status = order.create_order(request)  # Create new Order in database

        # Redirect to payment gateway(bank or others)
        if status:
            return redirect('order:bank')

        return HttpResponseNotFound()


# BankView
class CreateBankView(View):
    def get(self, request):
        try:
            oid = request.session['order']['oid']
            order = Order.objects.get(oid=oid)
        except (Order.DoesNotExist, KeyError):
            return HttpResponse('اتصال به درگاه پرداخت با مشکل مواجه شد. لطفا مجدد تلاش کنید')

        amount = int(order.payable_price)
        user_mobile_number = str(request.user.mobile)

        factory = bankfactories.BankFactory()
        try:
            bank = factory.auto_create()
            bank.set_request(request)
            bank.set_amount(amount)
            bank.set_client_callback_url(reverse('order:callback'))
            bank.set_mobile_number(user_mobile_number)

            bank_record = bank.ready()

            return bank.redirect_gateway()
        except (AZBankGatewaysException, TimeoutError):
            return HttpResponse('اتصال به درگاه پرداخت با مشکل مواجه شد. لطفا مجدد تلاش کنید')


# Render BankCallBackView
class CallBackView(LoginRequiredMixin, TemplateView):
    template_name = 'order/order_success.html'
    content_type = 'text/html'

    def dispatch(self, request, *args, **kwargs):
        tracking_code = request.GET.get(settings.TRACKING_CODE_QUERY_PARAM, None)

        try:
            order = Order.objects.get(oid=request.session['order']['oid'])
            order_items = OrderItem.objects.filter(order=order)
        except Order.DoesNotExist:
            raise Http404

        if not tracking_code:
            raise Http404

        try:
            bank_record = bank_models.Bank.objects.get(tracking_code=tracking_code)
        except bank_models.Bank.DoesNotExist:
            raise Http404

        if not bank_record.is_success:
            return HttpResponse('پرداخت با مشکل مواجه شد! در صورت کسر مبلغ تا ۴۸ ساعت آینده به حساب شما بازگردانده میشود.')

        # Modify new order to successful
        order.is_paid = True
        order.status = 'successful'
        order.bank_tracking_code = tracking_code
        order.save()

        cart = ModelCart(request)
        cart.cart_delete()  # Delete user cart from database

        # Try to minus Product quantity
        try:
            for item in order_items.all():
                product = ProductCustom.objects.get(idkc=item.product.idkc)
                product.quantity -= item.quantity
                product.save()
        except (ProductCustom.DoesNotExist, ProductCustom.MultipleObjectsReturned):
            raise Http404

        return super(CallBackView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        contexts = super().get_context_data(**kwargs)

        order = get_object_or_404(Order, oid=self.request.session['order']['oid'])
        address = get_object_or_404(Address, user=self.request.user, active=True)
        contexts['order'] = order
        contexts['address'] = address

        return contexts
