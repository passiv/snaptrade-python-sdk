from types import SimpleNamespace
import time
from datetime import datetime, timezone
import json

class SnapTradeUtils:
    @classmethod
    def convert_to_simple_namespace(cls, data):
        """Converts json data into python object"""
        if type(data) == dict:
            serialized_data = json.dumps(data)
        else:
            serialized_data = data

        return json.loads(serialized_data, object_hook=lambda d: SimpleNamespace(**d))

    @classmethod
    def get_api_endpoints(cls):
        with open('./snaptrade/api_client/endpoints.json', 'r') as f:
            return json.load(f)

    @classmethod
    def get_epoch_time(cls):
        return int(time.time())

    @classmethod
    def get_utc_time(cls, string_format=None):
        if string_format:
            return datetime.now(timezone.utc).strftime(string_format)
        else:
            return datetime.now(timezone.utc)
