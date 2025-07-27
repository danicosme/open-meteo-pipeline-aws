import requests
from loguru import logger


class ApiService:
    def __init__(self, url):
        self.url = url

    def get_response(self, params):
        try:
            response = requests.get(self.url, params=params)
            return response.json()
        except Exception as e:
            logger.error(f"An error occurred: {e}")
