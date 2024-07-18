from flask import Flask, render_template, request

from service import ForecastService


app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        city = request.form['city']
        result = ForecastService.get_coordinates(city)
        if not result.get('success'):
            error_msg = result.get('message')
            if error_msg:
                return render_template('index.html', error_message=error_msg)
        lat = result.get('latitude')
        lng = result.get('longitude')
        if lat and lng:
            forecast = ForecastService.get_forecast(lat, lng)
            return render_template('index.html', forecast_data=forecast)


if __name__ == '__main__':
    app.run(debug=True)
