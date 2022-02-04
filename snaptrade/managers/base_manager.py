from snaptrade.api_client import SnapTradeAPIClient
from snaptrade.models import APIStatus

class BaseManager():
    def __init__(self, client_id, consumer_key, return_response_as_dict=True):
        self.client_id = client_id
        self.consumer_key = consumer_key
        self.return_response_as_dict = return_response_as_dict

        self.api_client = SnapTradeAPIClient(self.client_id, self.consumer_key, self.return_response_as_dict)

    def get_api_status(self):
        status = self.api_client.api_status()
        return APIStatus.init_from_status_details(status)