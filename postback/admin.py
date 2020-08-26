from django.contrib import admin
from .models import Postback, Log


@admin.register(Postback)
class PostbackAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'affiliate',
        'offer',
        'status',
        'goal',
        'url',
    )


@admin.register(Log)
class LogAdmin(admin.ModelAdmin):
    list_display = (
        'created_at',
        'affiliate',
        'url',
        'response_status',
    )
