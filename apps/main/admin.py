from django.utils.translation import gettext_lazy as _
from django.contrib import admin


# Disable nav_sidebar
admin.site.enable_nav_sidebar = False


# Rename admin header & title & index_title
admin.site.site_header = _("Shop Management")
admin.site.site_title = _("Shop Management")
admin.site.index_title = _("Admin Panel")


# Add Custom delete action
@admin.action(description=_("Delete selected items"))
def delete_selected(modeladmin, request, queryset):
    queryset.delete()


admin.site.add_action(delete_selected)
