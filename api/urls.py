from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views.conversions import ConversionCreateView
from .views.offer import OfferViewSet
from .views.payout import PayoutViewSet
from .views.landing import LandingViewSet
from .views.offer_traffic_source import OfferTrafficSourceViewSet
from .views.advertiser import AdvertiserViewSet


router = DefaultRouter()
router.register(r'offers', OfferViewSet, basename="offer")
router.register(r'advertisers', AdvertiserViewSet, basename="advertiser")
router.register(r'landings', LandingViewSet, basename="landing")
router.register(r'payouts', PayoutViewSet, basename="payout")
router.register(
    r'traffic-sources',
    OfferTrafficSourceViewSet, basename="traffic-source"
)


urlpatterns = [
    path('', include(router.urls)),
    path(
        'conversions/',
        ConversionCreateView.as_view(), name='api-conversions'),
]
