from django.contrib import admin
from .models import (
    Offer,
    Category,
    TrafficSource,
    OfferTrafficSource,
    Goal,
    Currency,
    Payout,
    Advertiser,
    STOPPED_STATUS,
)


class OfferTrafficSource_inline(admin.TabularInline):
    model = OfferTrafficSource
    extra = 1


class Payout_inline(admin.TabularInline):
    model = Payout
    extra = 1


def duplicate_offer(modeladmin, request, queryset):
    for offer in queryset:
        source_payouts = [p for p in offer.payouts.all()]
        source_countries = [c for c in offer.countries.all()]
        source_categories = [c for c in offer.categories.all()]
        source_ots = [ots for ots in offer.offertrafficsource_set.all()]

        offer.id = None
        offer.title = offer.title + ' DUPLICATE'
        offer.status = STOPPED_STATUS
        offer.save()

        for country in source_countries:
            offer.countries.add(country)

        for category in source_categories:
            offer.categories.add(category)

        for payout in source_payouts:
            source_payout_countries = [c for c in payout.countries.all()]

            payout.id = None
            payout.save()

            for country in source_payout_countries:
                payout.countries.add(country)

            offer.payouts.add(payout)

        for ots in source_ots:
            ots.id = None
            ots.save()
            offer.offertrafficsource_set.add(ots)
    # queryset.update(status=PAUSED_STATUS)


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
