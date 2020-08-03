from django.urls import path
from .views import countries, categories


urlpatterns = [
    path('countries/', countries.CountryListView.as_view(), name='countries'),
    path(
        'categories/',
        categories.CategoryListView.as_view(), name='categories'),
]
