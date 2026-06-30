from django.urls import path
from . import views

app_name = 'weather'

urlpatterns = [
    path('', views.weather_home, name='home'),
    path('api/current/', views.get_weather_data, name='api_current'),
    path('api/forecast/', views.get_forecast_data, name='api_forecast'),
    path('api/search/', views.search_cities, name='api_search'),
]
