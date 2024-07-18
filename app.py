from flask import Flask, render_template, request
import openmeteo_requests
import requests
import requests_cache
from retry_requests import retry

from utils import get_coordinates


# cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
# retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
# openmeteo = openmeteo_requests.Client(session = retry_session)

app = Flask(__name__)

API_URL = "https://api.open-meteo.com/v1/forecast"
API_PARAMS = {
    'latitude': '',
    'longitude': '',
    'hourly': ['temperature_2m', 'precipitation',],
    'forecast_days': 1,
}

@app.route('/', methods=['GET', 'POST'])
def index():
    weather_data = {}
    if request.method == 'POST':
        city = request.form['city']
        result = get_coordinates(city)
        if not result.get('success'):
            error_msg = result.get('message')
            if error_msg:
                return render_template('index.html', error_message=error_msg)
        lat = result['latitude']
        lng = result['longitude']
        if lat and lng:
            API_PARAMS['latitude'] = lat
            API_PARAMS['longitude'] = lng
            response = requests.get(API_URL, params=API_PARAMS)
            if response.status_code == 200:
                data = response.json()
                temp_range = data['hourly']['temperature_2m']
                weather_data['min_temp'], weather_data['max_temp'] = min(temp_range), max(temp_range)
                weather_data['precipitation'] = int(sum(data['hourly']['precipitation']))
                return render_template('index.html', weather_data=weather_data)


if __name__ == '__main__':
    app.run(debug=True)