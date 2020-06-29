from django.urls import path

from .views.profile import AffiliateRetrieveAPIView
from .views.register import CreateUserView
from .views.offers import OfferListView, OfferRetrieveView, TrackingLinkView
from .views.stats import DailyStatsView, OffersStatsView
from .views.conversions import ConversionListView


urlpatterns = [
    path(
        'profile/',
        AffiliateRetrieveAPIView.as_view(), name='affiliate-profile'),
    path(
        'sign-up/',
        CreateUserView.as_view(), name='affiliate-sign-up'),
    path(
        'offers/', OfferListView.as_view(), name='affiliate-offers'),
    path(
        'offers/<int:pk>/',
        OfferRetrieveView.as_view(), name='affiliate-offer'),
    path(
        'offers/<int:pk>/tracking-link/',
        TrackingLinkView.as_view(), name='affiliate-offer-tracking-link'),
    path(
        'stats/daily/',
        DailyStatsView.as_view(), name='affiliate-stats-daily'),
    path(
        'stats/offers/',
        OffersStatsView.as_view(), name='affiliate-stats-offers'),
    path(
        'conversions/',
        ConversionListView.as_view(), name='affiliate-conversions'),
]
