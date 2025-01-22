import os

from src.templates.singleton import Singleton


class Config(Singleton):
    def __init__(self):
        self.api_url = os.environ.get('API_URL', '')
        self.api_key = os.environ.get('API_KEY', '')
