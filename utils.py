import os

from dotenv import load_dotenv
from opencage.geocoder import OpenCageGeocode


load_dotenv()


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
    