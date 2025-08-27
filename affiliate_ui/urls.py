from django.urls import path
from .views import AffiliateLoginView, dashboard, offer_list, offer_detail

urlpatterns = [
    path('login/', AffiliateLoginView.as_view(), name='login'),
    path('dashboard/', dashboard, name='dashboard'),
    path('offers/', offer_list, name='offer_list'),
    path('offers/<int:offer_id>/', offer_detail, name='offer_detail'),
]
