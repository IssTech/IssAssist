from django.contrib import admin

# Register your models here.
from .models import CoreConfig

class CoreConfigAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'hostname',
        'fqdn',
        'ipv4_address',
        ]

    class Meta:
        model = CoreConfig
admin.site.register(CoreConfig, CoreConfigAdmin)
