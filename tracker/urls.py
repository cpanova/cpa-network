from django.urls import path

from . import views


urlpatterns = [
    path('click', views.click, name='tracker-click'),
    path('postback', views.postback, name='tracker-postback'),
]
