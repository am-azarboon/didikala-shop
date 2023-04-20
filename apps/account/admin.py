from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import Group
from .models import User
from django.contrib import admin


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('mobile', 'email', 'access_level', 'is_active',)
    list_display_links = ('email', 'mobile',)
    list_filter = ('is_admin', 'is_active', 'access_level')
    fieldsets = (
        (None, {'fields': ('email', 'password',)}),
        (_('Personal info'), {'fields': ('mobile',)}),
        (_('Permissions'), {'fields': ('is_admin', 'is_active', 'access_level')}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('mobile', 'email', 'password1', 'password2'),
        }),
    )
    # Add search fields and ordering fields
    search_fields = ('mobile', 'email')
    ordering = ('mobile',)
    filter_horizontal = ()


# Since we're not using Django's built-in permissions, Unregister the Group model from admin.
admin.site.unregister(Group)
