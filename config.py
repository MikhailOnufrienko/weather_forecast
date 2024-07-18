import os

from dotenv import load_dotenv


load_dotenv()


class ForecastConfig:
    OPENCAGE_KEY = os.getenv('OPENCAGE_GEODATA_API_KEY')
    API_URL = "https://api.open-meteo.com/v1/forecast"
    API_PARAMS = {
        'latitude': '',
        'longitude': '',
        'hourly': ['temperature_2m', 'precipitation',],  # температура и кол-во осадков
        'forecast_days': 1,  # кол-во дней для прогноза
    }
