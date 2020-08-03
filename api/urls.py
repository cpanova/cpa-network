from django.urls import path
from .views.conversions import ConversionCreateView


urlpatterns = [
    path(
        'conversions/',
        ConversionCreateView.as_view(), name='api-conversions'),
]
