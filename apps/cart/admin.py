from .models import Cart, CartItem
from django import admin


# CartItem Admin
class CartItemInline(admin.StackedInline):
    model = CartItem
    extra = 0


# Cart ModelAdmin
@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at', 'updated_at',)
    list_display_links = ('user',)
    search_fields = ('user',)
    inlines = (CartItemInline,)
