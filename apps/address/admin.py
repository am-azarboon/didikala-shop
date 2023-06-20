from .models import Address, Province, City
from django import admin


# Register user Address
@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('user', 'fullname', 'mobile', 'province', 'post_code', 'active')
    list_display_links = ('user', 'fullname', 'mobile')
    readonly_fields = ('created_at', 'updated_at')


# Register Province/City to admin panel
admin.site.register(Province)
admin.site.register(City)
