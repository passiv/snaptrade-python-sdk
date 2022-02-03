import hmac
import json
import requests
from copy import deepcopy
from base64 import b64encode
from hashlib import sha256
from urllib.parse import urlencode
from snaptrade.utils import SnapTradeUtils

class SnapTradeAPIClient:
    api_version = "v1/"
    base_url = "https://api.passiv.com/api/"
    endpoints = SnapTradeUtils.get_api_endpoints()

    def __init__(self, client_id, consumer_key, return_response_as_dict=True, debug_response=False):
        self.client_id = client_id
        self.consumer_key = consumer_key
        self.return_response_as_dict = return_response_as_dict
        self.debug_response = debug_response

    def sign_request(self, request_data, request_path, request_query):
        sig_object = {"content": request_data, "path": request_path, "query": request_query}

        sig_content = json.dumps(sig_object, separators=(",", ":"), sort_keys=True)

        sig_digest = hmac.new(self.consumer_key.encode(), sig_content.encode(), sha256).digest()

        signature = b64encode(sig_digest).decode()

        return signature

    def get_signature(self, request_data, request_path=None, request_query=None):
        if request_query:
            request_query_string = urlencode(request_query)
        else:
            request_query_string = ""

        return self.sign_request(request_data, request_path, request_query_string)

    def _generate_request_path(self, endpoint_name, **path_params):
        """Generates API endpoint based on endpoint_name and params given"""
        endpoint = self.endpoints[endpoint_name]

        return "/api/v1/%s" % (endpoint["endpoint"] % path_params)  # type: ignore

    def _generate_api_endpoint(self, endpoint_name, **path_params):
        """Generates API endpoint based on endpoint_name and params given"""
        endpoint = self.endpoints[endpoint_name]

        return "%s%s%s" % (self.base_url, self.api_version, endpoint["endpoint"] % path_params,)

    def prepare_query_params(self, endpoint_name, initial_params=None):
        if initial_params:
            prepared_params = deepcopy(initial_params)
        else:
            prepared_params = dict()

        prepared_params["clientId"] = self.client_id
        prepared_params["timestamp"] = SnapTradeUtils.get_epoch_time()

        return prepared_params

    def _make_request(self, endpoint_name, data=None, path_params=None, query_params=None):
        if path_params is None:
            path_params = {}

        request_path = self._generate_request_path(endpoint_name, **path_params)

        signature = self.get_signature(data, request_path, query_params)

        endpoint = self._generate_api_endpoint(endpoint_name, **path_params)

        headers = {"Signature": signature}

        method = self.endpoints[endpoint_name]["method"]

        if method == "post":
            response = requests.post(endpoint, headers=headers, params=query_params, json=data)
        elif method == "get":
            response = requests.get(endpoint, headers=headers, params=query_params)
        elif method == "put":
            response = requests.put(endpoint, headers=headers, params=query_params, json=data)
        elif method == "delete":
            response = requests.delete(endpoint, headers=headers, params=query_params, json=data)

        if self.debug_response:
            return response

        if self.return_response_as_dict:
            return response.json()
        else:
            return SnapTradeUtils.convert_to_simple_namespace(response.content)





    def register_user(self, userId):
        """
        Register a new user in SnapTrade.

        A new userSecret will be generated if a user with the same userId already exists
        """
        endpoint_name = "register_user"

        data = dict(userId=userId)
        query_params = self.prepare_query_params(endpoint_name)

        return self._make_request(endpoint_name, query_params=query_params, data=data)

    def delete_user(self, userId, userSecret):
        """
        Register a new user in SnapTrade.

        A new userSecret will be generated if a user with the same userId already exists
        """
        endpoint_name = "delete_user"

        data = dict(userId=userId, userSecret=userSecret)
        query_params = self.prepare_query_params(endpoint_name)

        return self._make_request(endpoint_name, query_params=query_params, data=data)

    def generate_new_user_secret(self, userId):
        """
        Generate a new user secret for an existing user.

        If an existing user with userId doesn't exist, one will be created
        """
        endpoint_name = "register_user"

        data = dict(userId=userId)
        query_params = self.prepare_query_params(endpoint_name)

        return self._make_request(endpoint_name, query_params=query_params, data=data)

    def get_user_login_redirect_uri(self, userId, userSecret):
        endpoint_name = "user_login_redirect_uri"

        query_params = self.prepare_query_params(endpoint_name)

        data = dict(userId=userId, userSecret=userSecret)

        return self._make_request(endpoint_name, query_params=query_params, data=data)

    def get_all_holdings(self, userId, account_numbers=None):
        endpoint_name = "holdings"

        intial_query_params = {"userId":userId}

        if account_numbers:
            ",".join(account_numbers)
            intial_query_params["accounts"] = accounts

        query_params = self.prepare_query_params(endpoint_name, initial_params=intial_query_params)

        return self._make_request(endpoint_name, query_params=query_params)