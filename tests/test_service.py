import pytest
import requests
import requests_mock
from service import ForecastService
from config import ForecastConfig

# @pytest.fixture
# def mock_env(monkeypatch):
#     monkeypatch.setenv('OPENCAGE_GEODATA_API_KEY', 'test_api_key')

def test_get_coordinates_success(mocker):
    mocker.patch('opencage.geocoder.OpenCageGeocode.geocode', return_value=[{
        'geometry': {'lat': 52.52, 'lng': 13.405},
        'formatted': 'Berlin, Germany'
    }])
    
    result = ForecastService.get_coordinates('Berlin')
    assert result['success'] is True
    assert result['latitude'] == 52.52
    assert result['longitude'] == 13.405
    assert result['formatted_city_name'] == 'Berlin, Germany'

def test_get_coordinates_invalid_city(mocker):
    mocker.patch('opencage.geocoder.OpenCageGeocode.geocode', return_value=[])
    
    result = ForecastService.get_coordinates('InvalidCity')
    assert result['success'] is False
    assert 'Попробуйте ввести название реального города' in result['message']

def test_get_forecast_success():
    with requests_mock.Mocker() as m:
        m.get(ForecastConfig.API_URL, json={
            'hourly': {
                'temperature_2m': [10, 12, 15, 18, 20],
                'precipitation': [0.0, 0.5, 1.3, 1.2, 0.5, 0.0]
            }
        })
        
        result = ForecastService.get_forecast(52.52, 13.405)
        assert result['min_temp'] == 10
        assert result['max_temp'] == 20
        assert result['precipitation'] == 3
