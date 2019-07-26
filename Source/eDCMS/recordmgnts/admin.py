from django.contrib import admin
from .models import Container


class ContainerAdmin(admin.ModelAdmin):
    list_display = ('container_serial_number', 'container_description', 'is_active', 'created_by', 'created_date',
                    'modify_by', 'modify_date', 'warehouse')


admin.site.register(Container, ContainerAdmin)
admin.site.site_url = '/home'