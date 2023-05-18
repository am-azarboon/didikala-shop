from .models import Order, OrderItem
from django.contrib import admin


# Register OrderItem as Inline
class OrderItemInline(admin.StackedInline):
    model = OrderItem
    readonly_fields = ('quantity', 'total_price')
    extra = 1


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'quantity', 'payable_price', 'is_paid', 'status')
    list_display_links = ('user', 'quantity',)
    readonly_fields = ('payable_price', 'discount_price', 'is_paid', 'status', 'address_info', 'created_at')
    inlines = (OrderItemInline,)
