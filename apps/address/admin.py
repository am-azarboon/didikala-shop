from .models import Address, Province, City
from django.contrib import admin


# Register user Address
@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('user', 'firstname', 'lastname', 'province', 'post_code')
    list_display_links = ('user', 'firstname', 'lastname')
    readonly_fields = ('created_at', 'updated_at')


# # Register Province/City to admin panel
# admin.site.register(Province)
# admin.site.register(City)
