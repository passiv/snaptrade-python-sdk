from types import SimpleNamespace
import time
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
