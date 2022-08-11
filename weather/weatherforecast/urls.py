from django.urls import path

from .views import *

urlpatterns = [
    path('', RegionListView.as_view(), name='regions'),
    path('regrion/<slug:reg_slug>/', SingleRegionView.as_view(), name='region'),
    path('city/<slug:city_slug>/now', WeatherNowView.as_view(), name='city_now'),
    path('city/<slug:city_day_slug>/<int:day_num>', WeatherDayView.as_view(), name='day_weather'),
    path('city/<slug:city_five_slug>/five-days', FiveDayView.as_view(), name='five_days'),
]