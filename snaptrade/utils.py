from types import SimpleNamespace
import time
import json

class SnapTradeUtils:

    @classmethod
    def convert_to_simple_namespace(cls, data):
        """Converts json data into python object"""
        return SimpleNamespace(**data)

    @classmethod
    def get_api_endpoints(cls):
        with open('./snaptrade/endpoints.json', 'r') as f:
            return json.load(f)

    @classmethod
    def get_epoch_time(cls):
        return int(time.time())
