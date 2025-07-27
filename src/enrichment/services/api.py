import requests

class APIService:
    def __init__(self, url, headers=None, json=None):
        self.url = url
        self.headers = headers
        self.json = json

    def post(self):
        response = requests.post(
            url= self.url,
            headers=self.headers,
            json=self.json
        )
        return response.json()
    