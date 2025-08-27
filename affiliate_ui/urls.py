from django.urls import path
from .views.general_views import AffiliateLoginView, dashboard, offer_list, offer_detail
from .views.report_views import daily_report_view, offer_report_view, goal_report_view

urlpatterns = [
    path('login/', AffiliateLoginView.as_view(), name='login'),
    path('dashboard/', dashboard, name='dashboard'),
    path('offers/', offer_list, name='offer_list'),
    path('offers/<int:offer_id>/', offer_detail, name='offer_detail'),
    path('reports/daily/', daily_report_view, name='daily_report'),
    path('reports/offer/', offer_report_view, name='offer_report'),
    path('reports/goal/', goal_report_view, name='goal_report'),
]
