from unittest.mock import patch
from src.raw.services.api import ApiService
import json

expected_response = {
    "latitude": -23.5505,
    "longitude": -46.6333,
    "hourly": {"temperature_2m": [20, 21, 22]},
    "timezone": "America/Sao_Paulo",
}
params = {"city": "Sao Paulo"}
url = "http://test_api.com.br/api"

@patch("src.raw.services.api.requests.get")
def test_get_response_success(mock_get):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = expected_response
    api_service = ApiService(url)

    response = api_service.get_response(params=params)

    assert response == expected_response

@patch("src.raw.services.api.logger")
@patch("src.raw.services.api.requests.get")
def test_get_response_fail(mock_get, mock_logger):
    mock_get.return_value.status_code = 404
    mock_get.return_value.json.side_effect = Exception("Error during request")
    api_service = ApiService(url)

    api_service.get_response(params="error")

    mock_logger.error.assert_called_once_with("An error occurred: Error during request")
