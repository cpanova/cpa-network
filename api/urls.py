from django.urls import path
from .views.conversions import ConversionCreateView
from .views.offer import OfferCreateView
from .views.payout import PayoutCreateView


urlpatterns = [
    path(
        'conversions/',
        ConversionCreateView.as_view(), name='api-conversions'),
    path(
        'offers/',
        OfferCreateView.as_view(), name='api-offers'),
    path(
        'offers/<int:pk>/payouts/',
        PayoutCreateView.as_view(), name='api-payouts'),
]
