import pytest
from app import app


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


def test_index_get(client):
    response = client.get('/')
    assert response.status_code == 200


def test_index_post_success(client, mocker):
    mocker.patch('service.ForecastService.get_coordinates', return_value={
        'success': True,
        'latitude': 48.8534,
        'longitude': 2.3488,
        'formatted_city_name': 'Paris, France'
    })
    mocker.patch('service.ForecastService.get_forecast', return_value={
        'min_temp': 12,
        'max_temp': 20,
        'precipitation': 5
    })
    
    response = client.post('/', data={'city': 'Paris'})
    assert response.status_code == 200
    assert b'12' in response.data
    assert b'20' in response.data
    assert b'5' in response.data


def test_index_post_invalid_city(client):    
    response = client.post('/', data={'city': 'InvalidCity'})
    assert response.status_code == 200
    assert 'Введенное значение невалидно'.encode('utf-8') in response.data
