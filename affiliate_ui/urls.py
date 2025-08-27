from django.urls import path
from .views import AffiliateLoginView, dashboard, offer_list

urlpatterns = [
    path('login/', AffiliateLoginView.as_view(), name='login'),
    path('dashboard/', dashboard, name='dashboard'),
    path('offers/', offer_list, name='offer_list'),
]
