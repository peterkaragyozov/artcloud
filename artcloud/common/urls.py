from django.urls import path

from artcloud.common.views import LandingPage

urlpatterns = [
    path('', LandingPage.as_view(), name='index'),
]