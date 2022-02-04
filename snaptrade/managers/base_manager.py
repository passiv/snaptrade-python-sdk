from snaptrade.api_client import SnapTradeAPIClient

class BaseManager():
    def __init__(self, client_id, client_secret, return_response_as_dict=True):
        self.client_id = client_id
        self.client_secret = client_secret
        self.return_response_as_dict = return_response_as_dict

        self.api_client = SnapTradeAPIClient(self.client_id, self.client_secret, self.return_response_as_dict)