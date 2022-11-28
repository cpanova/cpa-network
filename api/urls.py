from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views.conversions import ConversionCreateView
from .views.offer import OfferViewSet
from .views.payout import PayoutCreateView
from .views.landing import LandingCreateView
from .views.offer_traffic_source import OfferTrafficSourceCreateView
from .views.advertiser import AdvertiserViewSet


router = DefaultRouter()
router.register(r'offers', OfferViewSet, basename="offer")
router.register(r'advertisers', AdvertiserViewSet, basename="advertiser")


urlpatterns = [
    path('', include(router.urls)),
    path(
        'conversions/',
        ConversionCreateView.as_view(), name='api-conversions'),
    path(
        'offers/<int:pk>/payouts/',
        PayoutCreateView.as_view(), name='api-payouts'),
    path(
        'offers/<int:pk>/landings/',
        LandingCreateView.as_view(), name='api-landings'),
    path(
        'offers/<int:pk>/traffic-sources/',
        OfferTrafficSourceCreateView.as_view(),
        name='api-offer-traffic-sources'),
]
