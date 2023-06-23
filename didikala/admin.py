from django.utils.translation import gettext_lazy as _
from django.contrib import admin

admin.site.site_header = _("Shop Management")
admin.site.site_title = _("Shop Management")
admin.site.index_title = _("Admin Panel")
admin.site.disable_action("delete_selected")
