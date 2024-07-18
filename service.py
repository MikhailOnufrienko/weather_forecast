import os

from dotenv import load_dotenv
from opencage.geocoder import OpenCageGeocode
import requests

from config import ForecastConfig


load_dotenv()


class ForecastService:    
    @staticmethod
    def get_coordinates(city: str) -> dict:
        try:
            key = os.getenv('OPENCAGE_GEODATA_API_KEY')
            geocoder = OpenCageGeocode(key)
            result = geocoder.geocode(city)[0]
            lat = result['geometry']['lat']
            lng = result['geometry']['lng']
            formatted_city_name = result['formatted']
            return {
                'success': True,
                'latitude': lat,
                'longitude': lng,
                'formatted_city_name': formatted_city_name
            }
        except IndexError:
            return {
                'success': False,
                'message': 'Введенное значение невалидно. Попробуйте ввести название реального города.'
            }
        except Exception as ex:
            return {
                'success': False,
                'message': ex
            }

    @staticmethod
    def get_forecast(latitude: float, longitude: float) -> dict:
        forecast_data = {}
        ForecastConfig.API_PARAMS['latitude'] = latitude
        ForecastConfig.API_PARAMS['longitude'] = longitude
        response = requests.get(ForecastConfig.API_URL, params=ForecastConfig.API_PARAMS)
        if response.status_code == 200:
            data = response.json()
            temp_range = data['hourly']['temperature_2m']
            forecast_data['min_temp'], forecast_data['max_temp'] = min(temp_range), max(temp_range)
            forecast_data['precipitation'] = int(sum(data['hourly']['precipitation']))
            return forecast_data
