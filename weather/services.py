"""
Weather Service Layer
Handles all weather API interactions with caching and error handling
"""
import requests
from django.core.cache import cache
from django.conf import settings
import logging
from datetime import datetime, timedelta
import hashlib
import random

logger = logging.getLogger(__name__)

class WeatherService:
    """
    Professional Weather API Service with caching, OSM Nominatim Geocoding,
    and pseudo-random consistent simulation fallback for Kisan Sathi.
    """
    
    BASE_URL = "https://api.openweathermap.org/data/2.5"
    
    def __init__(self):
        self.api_key = settings.OPENWEATHERMAP_API_KEY
        if not self.api_key:
            logger.warning("OpenWeatherMap API key not configured in settings")
        else:
            logger.info(f"Weather API initialized with key: {self.api_key[:8]}...")
            
    def reverse_geocode(self, lat, lon):
        """
        Reverse geocode coordinates using OSM Nominatim API to get location details
        """
        try:
            params = {
                'lat': lat,
                'lon': lon,
                'format': 'json',
                'addressdetails': 1,
                'accept-language': 'en'
            }
            
            headers = {
                'User-Agent': 'KisanSathiApp/1.0 (Banadeshwarareddy/kisan-sathi-ai-app)'
            }
            
            logger.info(f"Reverse geocoding via Nominatim for: {lat}, {lon}")
            
            response = requests.get(
                "https://nominatim.openstreetmap.org/reverse",
                params=params,
                headers=headers,
                timeout=5
            )
            
            if response.status_code == 200:
                data = response.json()
                address = data.get('address', {})
                name = (
                    address.get('village') or 
                    address.get('town') or 
                    address.get('city') or 
                    address.get('hamlet') or 
                    address.get('suburb') or 
                    address.get('municipality') or 
                    address.get('neighbourhood') or 
                    data.get('name') or 
                    'Detected Location'
                )
                district = address.get('state_district') or address.get('county') or ''
                state = address.get('state', '')
                country = address.get('country', '')
                return name, district, state, country
        except Exception as e:
            logger.error(f"Reverse geocode error: {str(e)}")
        return "Detected Location", "", "", ""
    
    def get_current_weather(self, city=None, lat=None, lon=None, location_name=None):
        """
        Get current weather data with caching and simulation fallback
        """
        if not self.api_key:
            logger.warning("No API key - returning simulated weather")
            return self._get_simulated_weather(city=city, lat=lat, lon=lon, location_name=location_name)
        
        # Create cache key
        loc_id = location_name or city or f"{lat},{lon}"
        safe_key = hashlib.md5(loc_id.encode('utf-8')).hexdigest()
        cache_key = f"weather_current_{safe_key}"
        cached_data = cache.get(cache_key)
        
        if cached_data:
            logger.info(f"Returning cached weather for {cache_key}")
            return cached_data
        
        try:
            params = {
                'appid': self.api_key,
                'units': 'metric'
            }
            
            if city:
                params['q'] = city
            elif lat and lon:
                params['lat'] = lat
                params['lon'] = lon
            else:
                return self._get_simulated_weather(city=city, lat=lat, lon=lon, location_name=location_name)
            
            logger.info(f"Fetching weather from API for: {city or f'{lat},{lon}'}")
            
            response = requests.get(
                f"{self.BASE_URL}/weather",
                params=params,
                timeout=10
            )
            
            logger.info(f"API Response Status: {response.status_code}")
            
            if response.status_code != 200:
                logger.error(f"API Error: {response.status_code} - {response.text}")
                return self._get_simulated_weather(city=city, lat=lat, lon=lon, location_name=location_name)
            
            response.raise_for_status()
            
            data = response.json()
            logger.info(f"Successfully fetched weather for: {data.get('name')}")
            
            weather_data = self._format_current_weather(data)
            
            # Override city if location_name is provided (e.g. detailed search result)
            if location_name:
                weather_data['city'] = location_name
            elif lat and lon and not city:
                # If using coordinates (e.g. My Location), resolve detailed name
                name, _, _, _ = self.reverse_geocode(lat, lon)
                if name:
                    weather_data['city'] = name
            
            # Cache for 10 minutes
            cache.set(cache_key, weather_data, 600)
            
            return weather_data
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Weather API error: {str(e)}")
            return self._get_simulated_weather(city=city, lat=lat, lon=lon, location_name=location_name)
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            return self._get_simulated_weather(city=city, lat=lat, lon=lon, location_name=location_name)
    
    def get_forecast(self, city=None, lat=None, lon=None, location_name=None):
        """
        Get 7-day weather forecast with caching and simulation fallback
        """
        if not self.api_key:
            logger.warning("No API key - returning simulated forecast")
            return self._get_simulated_forecast(city=city, lat=lat, lon=lon, location_name=location_name)
        
        loc_id = location_name or city or f"{lat},{lon}"
        safe_key = hashlib.md5(loc_id.encode('utf-8')).hexdigest()
        cache_key = f"weather_forecast_{safe_key}"
        cached_data = cache.get(cache_key)
        
        if cached_data:
            logger.info(f"Returning cached forecast for {cache_key}")
            return cached_data
        
        try:
            params = {
                'appid': self.api_key,
                'units': 'metric'
            }
            
            if city:
                params['q'] = city
            elif lat and lon:
                params['lat'] = lat
                params['lon'] = lon
            else:
                return self._get_simulated_forecast(city=city, lat=lat, lon=lon, location_name=location_name)
            
            logger.info(f"Fetching forecast from API for: {city or f'{lat},{lon}'}")
            
            response = requests.get(
                f"{self.BASE_URL}/forecast",
                params=params,
                timeout=10
            )
            
            logger.info(f"Forecast API Response Status: {response.status_code}")
            
            if response.status_code != 200:
                logger.error(f"Forecast API Error: {response.status_code} - {response.text}")
                return self._get_simulated_forecast(city=city, lat=lat, lon=lon, location_name=location_name)
            
            response.raise_for_status()
            data = response.json()
            
            logger.info(f"Successfully fetched forecast")
            
            # Format forecast to contain both daily and hourly precipitation
            daily_forecast = self._format_forecast(data)
            hourly_precip = self._extract_precipitation_prob(data)
            
            forecast_data = {
                'daily': daily_forecast,
                'hourly_precipitation': hourly_precip
            }
            
            # Cache for 30 minutes
            cache.set(cache_key, forecast_data, 1800)
            
            return forecast_data
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Forecast API error: {str(e)}")
            return self._get_simulated_forecast(city=city, lat=lat, lon=lon, location_name=location_name)
        except Exception as e:
            logger.error(f"Unexpected forecast error: {str(e)}")
            return self._get_simulated_forecast(city=city, lat=lat, lon=lon, location_name=location_name)
    
    def search_cities(self, query):
        """
        Search for locations (villages, towns, districts, cities) by name using OSM Nominatim API
        """
        if len(query) < 2:
            return []
        
        try:
            params = {
                'q': query,
                'format': 'json',
                'addressdetails': 1,
                'limit': 5,
                'accept-language': 'en'
            }
            
            headers = {
                'User-Agent': 'KisanSathiApp/1.0 (Banadeshwarareddy/kisan-sathi-ai-app)'
            }
            
            logger.info(f"Searching locations via Nominatim for: {query}")
            
            response = requests.get(
                "https://nominatim.openstreetmap.org/search",
                params=params,
                headers=headers,
                timeout=5
            )
            
            if response.status_code != 200:
                logger.error(f"Nominatim search error: {response.status_code} - {response.text}")
                return []
            
            results = response.json()
            logger.info(f"Found {len(results)} locations")
            
            cities = []
            for item in results:
                address = item.get('address', {})
                name = (
                    address.get('village') or 
                    address.get('town') or 
                    address.get('city') or 
                    address.get('hamlet') or 
                    address.get('suburb') or 
                    address.get('municipality') or 
                    address.get('neighbourhood') or 
                    item.get('name') or 
                    ''
                )
                if not name:
                    continue
                
                district = address.get('state_district') or address.get('county') or ''
                state = address.get('state', '')
                country = address.get('country', '')
                
                cities.append({
                    'name': name,
                    'district': district,
                    'state': state,
                    'country': country,
                    'lat': float(item.get('lat', 0)),
                    'lon': float(item.get('lon', 0)),
                    'display': f"{name}, {district}, {state}, {country}".strip(', ')
                })
            return cities
            
        except Exception as e:
            logger.error(f"Unexpected location search error: {str(e)}")
            return []
            
    def _get_simulated_weather(self, city=None, lat=None, lon=None, location_name=None):
        """
        Generate consistent, realistic simulated weather data for a location
        when the API key is missing or calls fail.
        """
        display_name = location_name
        country_code = "IN"
        
        if not display_name:
            if city:
                display_name = city.split(',')[0]
                if ',' in city:
                    country_code = city.split(',')[-1].upper()
            elif lat and lon:
                name, district, state, country = self.reverse_geocode(lat, lon)
                display_name = name
                country_code = "IN" if country.lower() == "india" else country[:2].upper()
            else:
                display_name = "Unknown Location"
                
        # Generate stable seed using hashlib of location name
        seed_str = f"{display_name}_{datetime.now().strftime('%Y-%m-%d')}"
        seed = int(hashlib.md5(seed_str.encode('utf-8')).hexdigest(), 16) % 100
        
        conditions = [
            ('Clear', '01d', '☀️', 'Sunny Day'),
            ('Clouds', '02d', '⛅', 'Partly Cloudy'),
            ('Clouds', '04d', '☁️', 'Overcast Clouds'),
            ('Rain', '10d', '🌦️', 'Light Rain'),
            ('Rain', '09d', '🌧️', 'Heavy Rain'),
            ('Thunderstorm', '11d', '⛈️', 'Thunderstorm with Rain'),
            ('Mist', '50d', '🌫️', 'Mist / Foggy')
        ]
        
        main_cond, icon, emoji, desc = conditions[seed % len(conditions)]
        
        month = datetime.now().month
        if 3 <= month <= 6:
            base_temp = 32
        elif 7 <= month <= 9:
            base_temp = 28
        else:
            base_temp = 22
            
        temp_var = (seed % 15) - 5
        temp = base_temp + temp_var
        feels_like = temp + (2 if main_cond in ['Rain', 'Clouds'] else 1)
        temp_min = temp - (seed % 4 + 2)
        temp_max = temp + (seed % 4 + 2)
        
        humidity = 45 + (seed % 45)
        pressure = 1005 + (seed % 15)
        wind_speed = round(5.0 + (seed % 25) * 0.8, 1)
        clouds = 10 + (seed % 80) if main_cond != 'Clear' else 5
        visibility = 10 - (seed % 5) if main_cond in ['Mist', 'Rain'] else 10
        
        return {
            'city': display_name,
            'country': country_code,
            'temperature': temp,
            'feels_like': feels_like,
            'temp_min': temp_min,
            'temp_max': temp_max,
            'humidity': humidity,
            'pressure': pressure,
            'wind_speed': wind_speed,
            'wind_deg': (seed * 15) % 360,
            'clouds': clouds,
            'visibility': visibility,
            'description': desc,
            'icon': icon,
            'main': main_cond,
            'sunrise': "05:45",
            'sunset': "18:50",
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'lat': float(lat) if lat else 22.7196,
            'lon': float(lon) if lon else 75.8577,
            'demo': True
        }
        
    def _get_simulated_forecast(self, city=None, lat=None, lon=None, location_name=None):
        """
        Generate consistent, realistic simulated forecast data
        """
        display_name = location_name
        if not display_name:
            if city:
                display_name = city.split(',')[0]
            elif lat and lon:
                display_name = "Detected Location"
            else:
                display_name = "Unknown Location"
                
        seed_str = f"{display_name}_{datetime.now().strftime('%Y-%m-%d')}_forecast"
        seed = int(hashlib.md5(seed_str.encode('utf-8')).hexdigest(), 16) % 100
        
        icons = ['01d', '02d', '03d', '10d', '01d', '02d', '01d', '09d', '11d', '50d']
        conditions = ['Sunny', 'Partly Cloudy', 'Cloudy', 'Light Rain', 'Sunny', 'Partly Cloudy', 'Sunny', 'Heavy Rain', 'Thunderstorm', 'Mist']
        
        month = datetime.now().month
        if 3 <= month <= 6:
            base_temp = 32
        elif 7 <= month <= 9:
            base_temp = 28
        else:
            base_temp = 22
            
        daily = []
        for i in range(7):
            date = datetime.now() + timedelta(days=i)
            day_seed = (seed + i * 7) % 100
            
            temp_var = (day_seed % 10) - 5
            temp_max = base_temp + temp_var + 3
            temp_min = base_temp + temp_var - 3
            
            cond_idx = day_seed % len(conditions)
            
            daily.append({
                'date': date.strftime('%Y-%m-%d'),
                'day': date.strftime('%a'),
                'temp_min': round(temp_min),
                'temp_max': round(temp_max),
                'condition': conditions[cond_idx],
                'icon': icons[cond_idx],
                'humidity': 50 + (day_seed % 40),
                'wind_speed': round(8.0 + (day_seed % 15), 1),
            })
            
        hourly = []
        for i in range(8):
            time_str = (datetime.now() + timedelta(hours=i*3)).strftime('%H:%M')
            pop_seed = (seed + i * 13) % 100
            pop = 0
            if conditions[seed % len(conditions)] in ['Light Rain', 'Heavy Rain', 'Thunderstorm']:
                pop = 30 + (pop_seed % 70)
            elif conditions[seed % len(conditions)] == 'Partly Cloudy':
                pop = pop_seed % 30
            else:
                pop = pop_seed % 10
                
            hourly.append({
                'time': time_str,
                'pop': pop
            })
            
        return {
            'daily': daily,
            'hourly_precipitation': hourly
        }

    def _format_current_weather(self, data):
        """Format API response to standardized structure"""
        return {
            'city': data.get('name'),
            'country': data.get('sys', {}).get('country'),
            'temperature': round(data.get('main', {}).get('temp', 0)),
            'feels_like': round(data.get('main', {}).get('feels_like', 0)),
            'temp_min': round(data.get('main', {}).get('temp_min', 0)),
            'temp_max': round(data.get('main', {}).get('temp_max', 0)),
            'humidity': data.get('main', {}).get('humidity', 0),
            'pressure': data.get('main', {}).get('pressure', 0),
            'wind_speed': round(data.get('wind', {}).get('speed', 0) * 3.6, 1),  # m/s to km/h
            'wind_deg': data.get('wind', {}).get('deg', 0),
            'clouds': data.get('clouds', {}).get('all', 0),
            'visibility': data.get('visibility', 0) // 1000,  # meters to km
            'description': data.get('weather', [{}])[0].get('description', '').title(),
            'icon': data.get('weather', [{}])[0].get('icon', '01d'),
            'main': data.get('weather', [{}])[0].get('main', 'Clear'),
            'sunrise': datetime.fromtimestamp(data.get('sys', {}).get('sunrise', 0)).strftime('%H:%M'),
            'sunset': datetime.fromtimestamp(data.get('sys', {}).get('sunset', 0)).strftime('%H:%M'),
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'lat': data.get('coord', {}).get('lat'),
            'lon': data.get('coord', {}).get('lon'),
        }
    
    def _format_forecast(self, data):
        """Format forecast data - Always return 7 days"""
        forecast_list = []
        
        if 'list' in data:
            daily_data = {}
            for item in data['list']:
                date = datetime.fromtimestamp(item['dt']).date()
                if date not in daily_data:
                    daily_data[date] = {
                        'temps': [],
                        'conditions': [],
                        'icons': [],
                        'humidity': [],
                        'wind': []
                    }
                daily_data[date]['temps'].append(item['main']['temp'])
                daily_data[date]['conditions'].append(item['weather'][0]['main'])
                daily_data[date]['icons'].append(item['weather'][0]['icon'])
                daily_data[date]['humidity'].append(item['main'].get('humidity', 0))
                daily_data[date]['wind'].append(item['wind'].get('speed', 0))
            
            sorted_dates = sorted(daily_data.keys())
            
            for date in sorted_dates:
                values = daily_data[date]
                forecast_list.append({
                    'date': date.strftime('%Y-%m-%d'),
                    'day': date.strftime('%a'),
                    'temp_min': round(min(values['temps'])),
                    'temp_max': round(max(values['temps'])),
                    'condition': max(set(values['conditions']), key=values['conditions'].count),
                    'icon': max(set(values['icons']), key=values['icons'].count),
                    'humidity': round(sum(values['humidity']) / len(values['humidity'])),
                    'wind_speed': round(sum(values['wind']) / len(values['wind']) * 3.6, 1),
                })
        
        while len(forecast_list) < 7:
            if len(forecast_list) > 0:
                last_day = forecast_list[-1]
                next_date = datetime.strptime(last_day['date'], '%Y-%m-%d').date() + timedelta(days=1)
                
                temp_variation = random.randint(-2, 2)
                
                forecast_list.append({
                    'date': next_date.strftime('%Y-%m-%d'),
                    'day': next_date.strftime('%a'),
                    'temp_min': last_day['temp_min'] + temp_variation,
                    'temp_max': last_day['temp_max'] + temp_variation,
                    'condition': last_day['condition'],
                    'icon': last_day['icon'],
                    'humidity': last_day.get('humidity', 65),
                    'wind_speed': last_day.get('wind_speed', 10),
                })
            else:
                # Fallback to simulated forecast if no data at all
                return self._get_simulated_forecast().get('daily')
        
        return forecast_list[:7]
 
    def _extract_precipitation_prob(self, data):
        """Extract precipitation probability for the next 24 hours (8 intervals of 3 hours)"""
        precip_data = []
        if 'list' in data:
            for item in data['list'][:8]:
                dt = datetime.fromtimestamp(item['dt'])
                time_str = dt.strftime('%H:%M')
                pop = round(item.get('pop', 0) * 100)
                precip_data.append({
                    'time': time_str,
                    'pop': pop
                })
        
        if len(precip_data) < 7:
            # Fallback will be handled by forecast returned structure
            pass
        return precip_data

    def get_farming_recommendations(self, weather_data):
        """
        Generate farming recommendations based on weather
        """
        temp = weather_data.get('temperature', 0)
        humidity = weather_data.get('humidity', 0)
        wind_speed = weather_data.get('wind_speed', 0)
        condition = weather_data.get('main', '')
        
        recommendations = []
        
        if temp > 35:
            recommendations.append({
                'type': 'warning',
                'icon': 'warning',
                'title': 'High Temperature Alert',
                'message': 'Increase irrigation frequency. Provide shade for sensitive crops.'
            })
        elif temp < 10:
            recommendations.append({
                'type': 'warning',
                'icon': 'ac_unit',
                'title': 'Cold Weather Alert',
                'message': 'Protect crops from frost. Consider covering sensitive plants.'
            })
        
        if 'Rain' in condition:
            recommendations.append({
                'type': 'info',
                'icon': 'umbrella',
                'title': 'Rain Expected',
                'message': 'Postpone irrigation. Good time for transplanting.'
            })
        
        if humidity > 80:
            recommendations.append({
                'type': 'caution',
                'icon': 'water_drop',
                'title': 'High Humidity',
                'message': 'Monitor for fungal diseases. Ensure good air circulation.'
            })
        
        if wind_speed > 30:
            recommendations.append({
                'type': 'warning',
                'icon': 'air',
                'title': 'Strong Winds',
                'message': 'Secure loose structures. Delay pesticide spraying.'
            })
        
        if 20 <= temp <= 30 and humidity < 70 and 'Clear' in condition:
            recommendations.append({
                'type': 'success',
                'icon': 'check_circle',
                'title': 'Ideal Farming Conditions',
                'message': 'Perfect weather for field operations and spraying.'
            })
        
        return recommendations
