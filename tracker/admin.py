from django.contrib import admin
from .models import Click, Conversion


admin.site.register(Click)


@admin.register(Conversion)
class ConversionAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'created_at',
        'affiliate',
        'offer',
        'revenue',
        'payout',
        'goal',
        'status',
        'ip',
        'country',
    )
