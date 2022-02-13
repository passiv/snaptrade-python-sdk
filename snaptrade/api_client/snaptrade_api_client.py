import hmac
import json
import requests
from copy import deepcopy
from base64 import b64encode
from hashlib import sha256
from urllib.parse import urlencode
from snaptrade.utils import SnapTradeUtils
from requests.exceptions import ConnectionError


class SnapTradeAPIClient:
    api_version = "v1/"
    base_url = "https://api.snaptrade.com/api/"
    endpoints = SnapTradeUtils.get_api_endpoints()

    def __init__(
        self,
        client_id,
        consumer_key,
        return_response_as_dict=True,
        debug_response=False,
    ):
        self.client_id = client_id
        self.consumer_key = consumer_key
        self.return_response_as_dict = return_response_as_dict
        self.debug_response = debug_response

    def sign_request(self, request_data, request_path, request_query):
        sig_object = {
            "content": request_data,
            "path": request_path,
            "query": request_query,
        }

        sig_content = json.dumps(sig_object, separators=(",", ":"), sort_keys=True)

        sig_digest = hmac.new(
            self.consumer_key.encode(), sig_content.encode(), sha256
        ).digest()

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

        return "%s%s%s" % (
            self.base_url,
            self.api_version,
            endpoint["endpoint"] % path_params,
        )

    def prepare_query_params(self, endpoint_name, initial_params=None):
        if initial_params:
            prepared_params = deepcopy(initial_params)
        else:
            prepared_params = dict()

        prepared_params["clientId"] = self.client_id
        prepared_params["timestamp"] = SnapTradeUtils.get_epoch_time()

        return prepared_params

    def _make_request(
        self, endpoint_name, data=None, path_params=None, query_params=None
    ):
        if path_params is None:
            path_params = {}

        request_path = self._generate_request_path(endpoint_name, **path_params)

        signature = self.get_signature(data, request_path, query_params)

        endpoint = self._generate_api_endpoint(endpoint_name, **path_params)

        headers = {"Signature": signature}

        method = self.endpoints[endpoint_name]["method"]

        response = None

        try:
            if method == "post":
                response = requests.post(
                    endpoint, headers=headers, params=query_params, json=data
                )
            elif method == "get":
                response = requests.get(endpoint, headers=headers, params=query_params)
            elif method == "put":
                response = requests.put(
                    endpoint, headers=headers, params=query_params, json=data
                )
            elif method == "delete":
                response = requests.delete(
                    endpoint, headers=headers, params=query_params, json=data
                )
        except ConnectionError:
            error_message = dict(
                status_code=502, detail="Failed to connect to api server", code=0000
            )
            if self.return_response_as_dict:
                return error_message
            else:
                return SnapTradeUtils.convert_to_simple_namespace(error_message)

        if self.debug_response:
            return response

        if response.content:
            data = response.json()
        else:
            data = dict(status_code=response.status_code, detail="No content returned")

        if self.return_response_as_dict:
            return data
        else:
            return SnapTradeUtils.convert_to_simple_namespace(data)

    """
    Gets API Status
    """

    def api_status(self):
        """Gets Snaptrade API status"""
        endpoint_name = "api_status"

        query_params = self.prepare_query_params(endpoint_name)

        return self._make_request(endpoint_name, query_params=query_params)

    """
    User registration, auth and deletion
    """

    def register_user(self, user_id):
        """
        Register a new user in SnapTrade.

        A new userSecret will be generated if a user with the same userId already exists
        """
        endpoint_name = "register_user"

        data = dict(userId=user_id)
        query_params = self.prepare_query_params(endpoint_name)

        return self._make_request(endpoint_name, query_params=query_params, data=data)

    def delete_user(self, user_id):
        """Deletes an existing user of provided user_id"""

        endpoint_name = "delete_user"

        initial_query_params = dict(userId=user_id)
        query_params = self.prepare_query_params(endpoint_name, initial_query_params)

        return self._make_request(endpoint_name, query_params=query_params)

    def get_user_login_redirect_uri(self, user_id, user_secret):
        """Returns redirect uri for user to"""
        endpoint_name = "user_login_redirect_uri"

        initial_query_params = dict(userId=user_id, userSecret=user_secret)
        query_params = self.prepare_query_params(
            endpoint_name, initial_params=initial_query_params
        )

        return self._make_request(endpoint_name, query_params=query_params)

    """
    Accounts details, holdings, activities, brokerage connection endpoints
    """

    def get_brokerage_connections(self, user_id, user_secret):
        endpoint_name = "brokerage_authorizations"

        initial_query_params = dict(userId=user_id, userSecret=user_secret)
        query_params = self.prepare_query_params(
            endpoint_name, initial_params=initial_query_params
        )

        return self._make_request(endpoint_name, query_params=query_params)

    def get_brokerage_connection_by_id(
        self, user_id, user_secret, brokerage_connection_id
    ):
        endpoint_name = "brokerage_authorization_by_id"

        initial_query_params = dict(userId=user_id, userSecret=user_secret)
        query_params = self.prepare_query_params(
            endpoint_name, initial_params=initial_query_params
        )

        path_params = dict(brokerage_authorization_id=brokerage_connection_id)

        return self._make_request(
            endpoint_name, path_params=path_params, query_params=query_params
        )

    def delete_brokerage_connection(
        self, user_id, user_secret, brokerage_connection_id
    ):
        endpoint_name = "delete_brokerage_authorization"

        initial_query_params = dict(userId=user_id, userSecret=user_secret)
        query_params = self.prepare_query_params(
            endpoint_name, initial_params=initial_query_params
        )

        path_params = dict(brokerage_authorization_id=brokerage_connection_id)

        return self._make_request(
            endpoint_name, path_params=path_params, query_params=query_params
        )

    def get_accounts(self, user_id, user_secret):
        endpoint_name = "accounts"
        initial_query_params = dict(userId=user_id, userSecret=user_secret)
        query_params = self.prepare_query_params(
            endpoint_name, initial_params=initial_query_params
        )

        return self._make_request(endpoint_name, query_params=query_params)

    def get_account_by_id(self, user_id, user_secret, account_id):
        endpoint_name = "account_details"
        initial_query_params = dict(userId=user_id, userSecret=user_secret)
        query_params = self.prepare_query_params(
            endpoint_name, initial_params=initial_query_params
        )
        path_params = dict(account_id=account_id)

        return self._make_request(
            endpoint_name, path_params=path_params, query_params=query_params
        )

    def get_account_balances(self, user_id, user_secret, account_id):
        endpoint_name = "account_balances"
        initial_query_params = dict(userId=user_id, userSecret=user_secret)
        query_params = self.prepare_query_params(
            endpoint_name, initial_params=initial_query_params
        )
        path_params = dict(account_id=account_id)

        return self._make_request(
            endpoint_name, path_params=path_params, query_params=query_params
        )

    def get_account_positions(self, user_id, user_secret, account_id):
        endpoint_name = "account_positions"
        initial_query_params = dict(userId=user_id, userSecret=user_secret)
        query_params = self.prepare_query_params(
            endpoint_name, initial_params=initial_query_params
        )
        path_params = dict(account_id=account_id)

        return self._make_request(
            endpoint_name, path_params=path_params, query_params=query_params
        )

    def get_account_holdings(self, user_id, user_secret, account_id):
        endpoint_name = "account_holdings"
        initial_query_params = dict(userId=user_id, userSecret=user_secret)
        query_params = self.prepare_query_params(
            endpoint_name, initial_params=initial_query_params
        )
        path_params = dict(account_id=account_id)

        return self._make_request(
            endpoint_name, path_params=path_params, query_params=query_params
        )

    def get_all_holdings(self, user_id, user_secret):
        endpoint_name = "holdings"
        initial_query_params = dict(userId=user_id, userSecret=user_secret)
        query_params = self.prepare_query_params(
            endpoint_name, initial_params=initial_query_params
        )

        return self._make_request(endpoint_name, query_params=query_params)

    def get_activities(self, user_id, user_secret, start_date=None, end_date=None):
        endpoint_name = "activities"

        initial_query_params = dict(userId=user_id, userSecret=user_secret)

        if start_date:
            initial_query_params["startDate"] = start_date

        if end_date:
            initial_query_params["endDate"] = end_date

        query_params = self.prepare_query_params(
            endpoint_name, initial_params=initial_query_params
        )

        return self._make_request(endpoint_name, query_params=query_params)

    """
    Reference data endpoints
    """

    def get_brokerages(self):
        endpoint_name = "brokerages"
        query_params = self.prepare_query_params(endpoint_name)

        return self._make_request(endpoint_name, query_params=query_params)

    def get_currencies(self):
        endpoint_name = "currencies"
        query_params = self.prepare_query_params(endpoint_name)

        return self._make_request(endpoint_name, query_params=query_params)

    def get_all_currencies_exchange_rates(self):
        endpoint_name = "currencies_rates"
        query_params = self.prepare_query_params(endpoint_name)

        return self._make_request(endpoint_name, query_params=query_params)

    def get_currency_pair_exchange_rate(self, src_currency_code, dst_currency_code):
        endpoint_name = "currency_pair_rate"
        query_params = self.prepare_query_params(endpoint_name)
        path_params = dict(currency_pair=f"{src_currency_code}-{dst_currency_code}")

        return self._make_request(
            endpoint_name, path_params=path_params, query_params=query_params
        )

    def search_symbols_by_name(self, substring):
        endpoint_name = "symbol_search"
        query_params = self.prepare_query_params(endpoint_name)
        data = dict(substring=substring)

        return self._make_request(endpoint_name, data=data, query_params=query_params)

    def get_symbol_details_by_universal_symbol_id(self, symbol_id):
        endpoint_name = "symbol_by_id"
        query_params = self.prepare_query_params(endpoint_name)
        path_params = dict(symbol_id=symbol_id)

        return self._make_request(
            endpoint_name, path_params=path_params, query_params=query_params
        )

    def get_symbol_details_by_ticker(self, ticker):
        endpoint_name = "symbol_by_ticker"
        query_params = self.prepare_query_params(endpoint_name)
        path_params = dict(ticker=ticker)

        return self._make_request(
            endpoint_name, path_params=path_params, query_params=query_params
        )

    """
    Trading endpoints
    """

    def get_market_quotes(
        self, user_id, user_secret, account_id, symbols, search_by_ticker=False
    ):
        endpoint_name = "symbol_quotes"

        symbols_string = ",".join(symbols)

        initial_query_params = dict(
            userId=user_id,
            userSecret=user_secret,
            symbols=symbols_string,
            use_ticker=search_by_ticker,
        )
        query_params = self.prepare_query_params(endpoint_name, initial_query_params)
        path_params = dict(account_id=account_id)

        return self._make_request(
            endpoint_name, path_params=path_params, query_params=query_params
        )

    def get_account_order_history(
        self, user_id, user_secret, account_id, state=None, days=None
    ):
        endpoint_name = "account_orders_history"

        initial_query_params = dict(userId=user_id, userSecret=user_secret)

        if state:
            initial_query_params["state"] = state

        if days:
            initial_query_params["days"] = days

        query_params = self.prepare_query_params(
            endpoint_name, initial_params=initial_query_params
        )
        path_params = dict(account_id=account_id)

        return self._make_request(
            endpoint_name, path_params=path_params, query_params=query_params
        )

    def get_trade_impact(
        self,
        user_id,
        user_secret,
        account_id,
        action,
        universal_symbol_id,
        order_type,
        time_in_force,
        units,
        price=None,
    ):
        endpoint_name = "trade_impact"

        initial_query_params = dict(userId=user_id, userSecret=user_secret)

        query_params = self.prepare_query_params(
            endpoint_name, initial_params=initial_query_params
        )

        if time_in_force.title() == "Day":
            time_in_force = time_in_force.title()

        trade_data = {
            "account_id": account_id,
            "action": action.title(),
            "universal_symbol_id": universal_symbol_id,
            "order_type": order_type,
            "time_in_force": time_in_force,
            "price": price,
            "units": units,
        }

        return self._make_request(
            endpoint_name, data=trade_data, query_params=query_params
        )

    def place_order(self, user_id, user_secret, trade_id):
        endpoint_name = "place_order"

        initial_query_params = dict(userId=user_id, userSecret=user_secret)

        query_params = self.prepare_query_params(
            endpoint_name, initial_params=initial_query_params
        )

        path_params = dict(trade_id=trade_id)

        return self._make_request(
            endpoint_name, path_params=path_params, query_params=query_params
        )

    def cancel_order(self, user_id, user_secret, account_id, brokerage_order_id):
        endpoint_name = "cancel_order"

        initial_query_params = dict(userId=user_id, userSecret=user_secret)

        query_params = self.prepare_query_params(
            endpoint_name, initial_params=initial_query_params
        )

        path_params = dict(account_id=account_id)

        data = dict(brokerage_order_id=brokerage_order_id)

        return self._make_request(
            endpoint_name, path_params=path_params, query_params=query_params, data=data
        )
