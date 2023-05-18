from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django_jalali.admin.filters import JDateFieldListFilter
from django.utils.translation import gettext_lazy as _
from .forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import Group
from .models import User, Profile
from django.contrib import admin


# Register the Profile model with custom ProfileAdmin to admin site
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_filter = (('date_of_birth', JDateFieldListFilter), 'created_at',)
    readonly_fields = ('created_at', 'updated_at',)
    list_display = ('user', 'firstname', 'lastname', 'melli_code', 'date_of_birth',)
    list_display_links = ('user', 'firstname', 'lastname',)
    fieldsets = (
        (None, {'fields': ('user', 'firstname', 'lastname', 'melli_code', 'gender',)}),
        (_('Additional info'), {'fields': ('date_of_birth', 'profile_image',)}),
        (_('Confirmations'), {'fields': ('is_foreign_citizen', 'is_subscriber',)}),
        (_('Register info'), {'fields': ('created_at', 'updated_at',)})
    )


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('mobile', 'email', 'access_level', 'is_active', 'verified',)
    list_display_links = ('email', 'mobile',)
    list_filter = ('is_active', 'access_level', 'verified',)
    fieldsets = (
        (None, {'fields': ('email', 'password',)}),
        (_('Personal info'), {'fields': ('mobile',)}),
        (_('Permissions'), {'fields': ('access_level', 'is_admin', 'is_active',)}),
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
