from flask import Flask
from flask import jsonify, render_template, request
from redis import Redis

from service import ForecastService


app = Flask(__name__)

redis_client = Redis(host='localhost', port=6379, db=0)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')
    if request.method == 'POST':
        city = request.form['city']
        result = ForecastService.get_coordinates(city)
        if not result.get('success'):
            error_msg = result.get('message')
            if error_msg:
                return render_template('index.html', error_message=error_msg)
        user_ip = request.remote_addr
        formatted_city = result.get('formatted_city_name')
        redis_client.lpush(user_ip, formatted_city)  # сохраняем в Redis отформатированное название
                                                     # введенного города, ключ - IP пользователя
        lat = result.get('latitude')
        lng = result.get('longitude')
        if lat and lng:
            forecast = ForecastService.get_forecast(lat, lng)
            return render_template('index.html', forecast_data=forecast)


@app.route('/autocomplete', methods=['GET'])
def autocomplete():
    user_ip = request.remote_addr
    term = request.args.get('term', '').lower()
    cities = redis_client.lrange(user_ip, 0, -1)  # получаем список введенных ранее городов
    cities = list(set(city.decode('utf-8') for city in cities if term in city.decode('utf-8').lower()))
    return jsonify(cities)


if __name__ == '__main__':
    app.run(debug=True)
