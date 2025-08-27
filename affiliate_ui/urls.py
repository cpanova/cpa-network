from django.urls import path
from .views import AffiliateLoginView, dashboard

urlpatterns = [
    path('login/', AffiliateLoginView.as_view(), name='login'),
    path('dashboard/', dashboard, name='dashboard'),
]
