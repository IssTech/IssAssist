from django.contrib import admin

# Register your models here.
from .models import IssSys

class IssSysAdmin(admin.ModelAdmin):
    list_display = [
        'host_id',
        'update_datetime',
        'isssys_version',
        'total_updates',
        'security_updates',
        'priority1_updates',
        'priority2_updates',
        'priority3_updates',
        'priority4_updates',
        'priority5_updates'
        ]

    class Meta:
        model = IssSys
admin.site.register(IssSys, IssSysAdmin)
