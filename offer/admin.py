from django.contrib import admin
from .models import (
    Offer,
    Category,
    TrafficSource,
    OfferTrafficSource,
    Goal,
    Currency,
    Payout,
    Advertiser
)


class OfferTrafficSource_inline(admin.TabularInline):
    model = OfferTrafficSource
    extra = 1


class Payout_inline(admin.TabularInline):
    model = Payout
    extra = 1


def duplicate_offer(modeladmin, request, queryset):
    for obj in queryset:
        obj.id = None
        obj.title = obj.title + ' DUPLICATE'
        obj.save()
    queryset.update(status='p')
duplicate_offer.short_description = "Duplicate"


@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
    inlines = (
        OfferTrafficSource_inline,
        Payout_inline,
    )
    list_display = (
        'title', 'id', 'status', 'advertiser',
    )
    actions = [duplicate_offer]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(TrafficSource)
class TrafficSourceAdmin(admin.ModelAdmin):
    pass


@admin.register(Goal)
class GoalAdmin(admin.ModelAdmin):
    pass


@admin.register(Payout)
class PayoutAdmin(admin.ModelAdmin):
    list_display = (
        'offer', 'revenue', 'payout', 'currency',
        'goal_value', 'goal',
    )


@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    pass


@admin.register(Advertiser)
class AdvertiserAdmin(admin.ModelAdmin):
    pass
