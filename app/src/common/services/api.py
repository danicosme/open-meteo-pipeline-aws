import requests
from loguru import logger


class ApiService:
    def __init__(self, url):
        self.url = url

    def get(self, params):
        try:
            response = requests.get(self.url, params=params)
            return response.json()
        except Exception as e:
            logger.error(f"An error occurred: {e}")
            raise e

    def post(self, headers, json):
        try:
            response = requests.post(url=self.url, headers=headers, json=json)
            return response.json()
        except Exception as e:
            logger.error(f"An error occurred: {e}")
            raise e
