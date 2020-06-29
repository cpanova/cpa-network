from django.urls import path
from .views.affiliates import AffiliateListView, AffiliateRetrieveView
from .views.offers import OfferListView, OfferRetrieveView
from .views.stats import DailyStatsView, OffersStatsView, AffiliatesStatsView
from .views.conversions import ConversionListView


urlpatterns = [
    path(
        'affiliates/',
        AffiliateListView.as_view(), name='network-affiliates'),
    path(
        'affiliates/<int:pk>/',
        AffiliateRetrieveView.as_view(), name='network-affiliate'),
    path('offers/', OfferListView.as_view(), name='network-offers'),
    path(
        'offers/<int:pk>/',
        OfferRetrieveView.as_view(), name='network-offer'),
    path(
        'stats/daily/',
        DailyStatsView.as_view(), name='network-stats-daily'),
    path(
        'stats/offers/',
        OffersStatsView.as_view(), name='network-stats-offers'),
    path(
        'stats/affiliates/',
        AffiliatesStatsView.as_view(), name='network-stats-affiliates'),
    path(
        'conversions/',
        ConversionListView.as_view(), name='network-conversions'),
]
