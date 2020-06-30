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


@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
    inlines = (OfferTrafficSource_inline,)
    list_display = (
        'title', 'id', 'status', 'advertiser',
    )


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
    pass


@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    pass


@admin.register(Advertiser)
class AdvertiserAdmin(admin.ModelAdmin):
    pass
