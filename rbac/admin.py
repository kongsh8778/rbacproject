from django.contrib import admin
from rbac import models


class PermissionAdmin(admin.ModelAdmin):
    list_display = ['title', 'url', 'menu', 'parent', 'alias']
    list_editable = ['url', 'alias']


admin.site.register(models.Permission, PermissionAdmin)
admin.site.register(models.Role)
admin.site.register(models.UserInfo)
admin.site.register(models.Menu)
