from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .services import WeatherService
import json

weather_service = WeatherService()

@login_required(login_url='accounts:login')
def weather_home(request):
    """Main weather page"""
    context = {
        'active_page': 'weather',
    }
    return render(request, 'weather/home.html', context)

@require_http_methods(["GET"])
def get_weather_data(request):
    """
    API endpoint to get current weather data
    Query params: city OR lat,lon AND optional location_name
    """
    city = request.GET.get('city')
    lat = request.GET.get('lat')
    lon = request.GET.get('lon')
    location_name = request.GET.get('location_name')
    
    if not city and not (lat and lon):
        return JsonResponse({
            'error': 'Please provide city name or coordinates'
        }, status=400)
    
    try:
        weather_data = weather_service.get_current_weather(
            city=city,
            lat=float(lat) if lat else None,
            lon=float(lon) if lon else None,
            location_name=location_name
        )
        
        if not weather_data:
            return JsonResponse({
                'error': 'Unable to fetch weather data'
            }, status=500)
        
        # Get farming recommendations
        recommendations = weather_service.get_farming_recommendations(weather_data)
        
        return JsonResponse({
            'success': True,
            'weather': weather_data,
            'recommendations': recommendations
        })
        
    except Exception as e:
        return JsonResponse({
            'error': str(e)
        }, status=500)

@require_http_methods(["GET"])
def get_forecast_data(request):
    """
    API endpoint to get 7-day forecast
    """
    city = request.GET.get('city')
    lat = request.GET.get('lat')
    lon = request.GET.get('lon')
    location_name = request.GET.get('location_name')
    
    if not city and not (lat and lon):
        return JsonResponse({
            'error': 'Please provide city name or coordinates'
        }, status=400)
    
    try:
        forecast_data = weather_service.get_forecast(
            city=city,
            lat=float(lat) if lat else None,
            lon=float(lon) if lon else None,
            location_name=location_name
        )
        
        return JsonResponse({
            'success': True,
            'forecast': forecast_data
        })
        
    except Exception as e:
        return JsonResponse({
            'error': str(e)
        }, status=500)

@require_http_methods(["GET"])
def search_cities(request):
    """
    API endpoint to search cities
    """
    query = request.GET.get('q', '')
    
    if len(query) < 2:
        return JsonResponse({
            'cities': []
        })
    
    try:
        cities = weather_service.search_cities(query)
        return JsonResponse({
            'success': True,
            'cities': cities
        })
        
    except Exception as e:
        return JsonResponse({
            'error': str(e)
        }, status=500)
