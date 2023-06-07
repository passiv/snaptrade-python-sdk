import hmac
import json
from base64 import b64encode
from copy import deepcopy
from hashlib import sha256
from urllib.parse import urlencode

import requests
from requests.exceptions import ConnectionError
from snaptrade.utils import SnapTradeUtils


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
        user_jwt=None,
    ):
        self.client_id = client_id
        self.consumer_key = consumer_key
        self.return_response_as_dict = return_response_as_dict
        self.debug_response = debug_response
        self.user_jwt = user_jwt

    @classmethod
    def jwt_init(cls, jwt, return_response_as_dict=True, debug_response=False):
        """Returns returns a SnapTradeAPIClient instance by passing in a JWT token. This will set the client_id and consumer_key to None"""
        return cls(None, None, return_response_as_dict, debug_response, jwt)

    def sign_request(self, request_data, request_path, request_query):
        """This method is responsible for signing request using the provided consumer key"""

        sig_object = {
            "content": request_data,
            "path": request_path,
            "query": request_query,
        }

        sig_content = json.dumps(sig_object, separators=(",", ":"), sort_keys=True)

        sig_digest = hmac.new(self.consumer_key.encode(), sig_content.encode(), sha256).digest()

        signature = b64encode(sig_digest).decode()

        return signature

    def get_signature(self, request_data, request_path=None, request_query=None):
        """Prepares request query string and get the signature of a request"""
        if request_query:
            request_query_string = urlencode(request_query)
        else:
            request_query_string = ""

        return self.sign_request(request_data, request_path, request_query_string)

    def _generate_request_path(self, endpoint_name, **path_params):
        """Generates API endpoint based on endpoint_name and params given"""
        endpoint = self.endpoints[endpoint_name]

        return "/api/v1/%s" % (endpoint["endpoint"] % path_params) 

    def _generate_api_endpoint(self, endpoint_name, **path_params):
        """Generates API endpoint based on endpoint_name and params given"""
        endpoint = self.endpoints[endpoint_name]

        return "%s%s%s" % (
            self.base_url,
            self.api_version,
            endpoint["endpoint"] % path_params,
        )

    def prepare_query_params(self, endpoint_name, initial_params=None):
        """Adds clientId and timestamp to the query params and returns it"""
        if initial_params:
            prepared_params = deepcopy(initial_params)
        else:
            prepared_params = dict()

        if self.user_jwt:
            if "userId" in prepared_params:
                prepared_params.pop("userId")
            if "userSecret" in prepared_params:
                prepared_params.pop("userSecret")
        else:
            prepared_params["clientId"] = self.client_id
            prepared_params["timestamp"] = SnapTradeUtils.get_epoch_time()

        return prepared_params

    def _make_request(self, endpoint_name, data=None, path_params=None, query_params=None, force_signature_auth=False):
        """Logic to make request to SnapTrade API server"""
        if path_params is None:
            path_params = {}

        request_path = self._generate_request_path(endpoint_name, **path_params)

        endpoint = self._generate_api_endpoint(endpoint_name, **path_params)

        if self.user_jwt and not force_signature_auth:
            headers = {"Authorization": f"JWT {self.user_jwt}"}
        else:
            signature = self.get_signature(data, request_path, query_params)
            headers = {"Signature": signature}

        method = self.endpoints[endpoint_name]["method"]
        
        response = None
 
        try:
            if method == "post":
                response = requests.post(endpoint, headers=headers, params=query_params, json=data)
            elif method == "get":
                response = requests.get(endpoint, headers=headers, params=query_params)
            elif method == "put":
                response = requests.put(endpoint, headers=headers, params=query_params, json=data)
            elif method == "delete":
                response = requests.delete(endpoint, headers=headers, params=query_params, json=data)
        except ConnectionError:
            error_message = dict(status_code=502, detail="Failed to connect to api server", code="0000")
            if self.return_response_as_dict:
                return error_message
            else:
                return SnapTradeUtils.convert_to_simple_namespace(error_message)

        if self.debug_response:
            return response

        if response.status_code == 502:
            error_message = dict(status_code=502, detail="Failed to connect to api server", code="0000")
            if self.return_response_as_dict:
                return error_message
            else:
                return SnapTradeUtils.convert_to_simple_namespace(error_message)

        try:
            if response.content:
                data = response.json()
            else:
                data = dict(status_code=response.status_code, detail="No content returned")
        except:
            data = dict(status_code=response.status_code, detail=f"{str(response.content)}", code="0000")


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
    User registration, auth and deletion, register users list
    """

    def get_registered_users(self):
        """
        Gets a list of SnapTrade users registered by partner
        """
        endpoint_name = "registered_users"

        query_params = self.prepare_query_params(endpoint_name)

        return self._make_request(endpoint_name, query_params=query_params, force_signature_auth=True)

    def register_user(self, user_id, rsa_public_key=None):
        """
        Register a new user in SnapTrade.

        A new userSecret will be generated if a user with the same userId already exists
        """
        endpoint_name = "register_user"

        data = dict(userId=user_id, rsaPublicKey=rsa_public_key)
        query_params = self.prepare_query_params(endpoint_name)

        return self._make_request(endpoint_name, query_params=query_params, data=data, force_signature_auth=True)

    def delete_user(self, user_id):
        """Deletes an existing user of provided user_id"""

        endpoint_name = "delete_user"

        initial_query_params = dict(userId=user_id)
        query_params = self.prepare_query_params(endpoint_name, initial_query_params)

        return self._make_request(endpoint_name, query_params=query_params, force_signature_auth=True)

    def get_encrypted_jwt(self, user_id, user_secret):
        """Returns encrypted JWT token"""
        endpoint_name = "get_encrypted_jwt"

        initial_query_params = dict(userId=user_id, userSecret=user_secret)
        query_params = self.prepare_query_params(endpoint_name, initial_params=initial_query_params)

        return self._make_request(endpoint_name, query_params=query_params, force_signature_auth=True)

    def get_user_login_redirect_uri(
        self,
        user_id,
        user_secret,
        broker=None,
        immediate_redirect=False,
        custom_redirect=None,
        reconnect = None,
        connection_type = None,
    ):
        """Returns redirect uri for user"""
        endpoint_name = "user_login_redirect_uri"

        initial_query_params = dict(userId=user_id, userSecret=user_secret)
        query_params = self.prepare_query_params(endpoint_name, initial_params=initial_query_params)

        data = dict()
        if broker:
            data["broker"] = broker
        if immediate_redirect:
            data["immediateRedirect"] = True
        if custom_redirect:
            data["customRedirect"] = custom_redirect
        if reconnect:
            data["reconnect"] = reconnect
        if connection_type:
            data["connectionType"] = connection_type

        if not data:
            data = None

        return self._make_request(endpoint_name, data=data, query_params=query_params, force_signature_auth=True)

    """
    Accounts details, holdings, brokerage connection endpoints
    """

    def get_brokerage_connections(self, user_id, user_secret):
        """Gets all brokerage connection (aka. authorization) the user has linked"""
        endpoint_name = "brokerage_authorizations"

        initial_query_params = dict(userId=user_id, userSecret=user_secret)
        query_params = self.prepare_query_params(endpoint_name, initial_params=initial_query_params)

        return self._make_request(endpoint_name, query_params=query_params)

    def get_brokerage_connection_by_id(self, user_id, user_secret, brokerage_connection_id):
        """Gets brokerage connection (aka. authorization) object by id"""
        endpoint_name = "brokerage_authorization_by_id"

        initial_query_params = dict(userId=user_id, userSecret=user_secret)
        query_params = self.prepare_query_params(endpoint_name, initial_params=initial_query_params)

        path_params = dict(brokerage_authorization_id=brokerage_connection_id)

        return self._make_request(endpoint_name, path_params=path_params, query_params=query_params)

    def delete_brokerage_connection(self, user_id, user_secret, brokerage_connection_id):
        """Deletes brokerage connection (aka. authorization) object by id"""
        endpoint_name = "delete_brokerage_authorization"

        initial_query_params = dict(userId=user_id, userSecret=user_secret)
        query_params = self.prepare_query_params(endpoint_name, initial_params=initial_query_params)

        path_params = dict(brokerage_authorization_id=brokerage_connection_id)

        return self._make_request(endpoint_name, path_params=path_params, query_params=query_params)

    def get_accounts(self, user_id, user_secret):
        """Gets all user's brokerage account"""
        endpoint_name = "accounts"
        initial_query_params = dict(userId=user_id, userSecret=user_secret)
        query_params = self.prepare_query_params(endpoint_name, initial_params=initial_query_params)

        return self._make_request(endpoint_name, query_params=query_params)

    def get_account_by_id(self, user_id, user_secret, account_id):
        """Gets brokerage account object by id"""
        endpoint_name = "account_details"
        initial_query_params = dict(userId=user_id, userSecret=user_secret)
        query_params = self.prepare_query_params(endpoint_name, initial_params=initial_query_params)
        path_params = dict(account_id=account_id)

        return self._make_request(endpoint_name, path_params=path_params, query_params=query_params)

    def get_account_balances(self, user_id, user_secret, account_id):
        """Gets balances for a brokerage account"""
        endpoint_name = "account_balances"
        initial_query_params = dict(userId=user_id, userSecret=user_secret)
        query_params = self.prepare_query_params(endpoint_name, initial_params=initial_query_params)
        path_params = dict(account_id=account_id)

        return self._make_request(endpoint_name, path_params=path_params, query_params=query_params)

    def get_account_positions(self, user_id, user_secret, account_id):
        """Gets positions for a brokerage account"""
        endpoint_name = "account_positions"
        initial_query_params = dict(userId=user_id, userSecret=user_secret)
        query_params = self.prepare_query_params(endpoint_name, initial_params=initial_query_params)
        path_params = dict(account_id=account_id)

        return self._make_request(endpoint_name, path_params=path_params, query_params=query_params)

    def get_account_holdings(self, user_id, user_secret, account_id):
        """Gets holdings (balances, positions & orders) for a brokerage account"""
        endpoint_name = "account_holdings"
        initial_query_params = dict(userId=user_id, userSecret=user_secret)
        query_params = self.prepare_query_params(endpoint_name, initial_params=initial_query_params)
        path_params = dict(account_id=account_id)

        return self._make_request(endpoint_name, path_params=path_params, query_params=query_params)

    def get_all_holdings(self, user_id, user_secret, brokerage_authorization_ids=None, account_numbers=None):
        """Gets holdings (balances, positions & orders) acroos all brokerage accounts a user has"""
        endpoint_name = "holdings"
        initial_query_params = dict(userId=user_id, userSecret=user_secret)

        if brokerage_authorization_ids:
            brokerage_authorizations_ids_string = ",".join([str(auth_id) for auth_id in brokerage_authorization_ids])
            initial_query_params["brokerage_authorizations"] = brokerage_authorizations_ids_string
        if account_numbers:
            accounts_numbers_string = ",".join([str(account_number) for account_number in account_numbers])
            initial_query_params["accounts"] = accounts_numbers_string

        query_params = self.prepare_query_params(endpoint_name, initial_params=initial_query_params)

        return self._make_request(endpoint_name, query_params=query_params)

    """
    Reporting endpoints: activities, performance
    """

    def get_activities(self, user_id, user_secret, start_date=None, end_date=None, account_ids=None, type_filter=None):
        """Gets available activities/transactions of all brokerage accounts linked to the user"""
        endpoint_name = "activities"

        initial_query_params = dict(userId=user_id, userSecret=user_secret)

        if start_date:
            initial_query_params["startDate"] = start_date

        if end_date:
            initial_query_params["endDate"] = end_date
            
        if type_filter:
            initial_query_params["type"] = type_filter

        if account_ids:
            # Expects a list of account ids
            initial_query_params["accounts"] = ",".join([str(account_id) for account_id in account_ids])

        query_params = self.prepare_query_params(endpoint_name, initial_params=initial_query_params)

        return self._make_request(endpoint_name, query_params=query_params)

    def get_performance_custom(
        self, user_id, user_secret, start_date, end_date, frequency=None, accountIDs=None, account_ids=None
    ):
        """Gets performance information of all brokerage accounts linked to the user"""
        endpoint_name = "performance"

        initial_query_params = dict(userId=user_id, userSecret=user_secret, startDate=start_date, endDate=end_date)

        if frequency:
            initial_query_params["frequency"] = frequency

        if account_ids:
            # Expects a list of account ids
            initial_query_params["accounts"] = ",".join([str(account_id) for account_id in account_ids])
        elif accountIDs:
            # accountIDs is left in for backwards compatibility. We should be using account_ids moving forward

            # a comma separated string is expected for accountIDs
            initial_query_params["accounts"] = accountIDs

        query_params = self.prepare_query_params(endpoint_name, initial_params=initial_query_params)

        return self._make_request(endpoint_name, query_params=query_params)

    """
    Reference data endpoints
    """

    def get_brokerages(self):
        """Get a list of brokerages objects supported by SnapTrade"""
        endpoint_name = "brokerages"
        query_params = self.prepare_query_params(endpoint_name)

        return self._make_request(endpoint_name, query_params=query_params)

    def get_brokerage_authorization_types(self, brokerages=None):
        """Get a list of brokerages authorization (aka connection) types supported by SnapTrade"""
        endpoint_name = "brokerage_authorization_types"

        brokerages_string = ""

        if brokerages:
            brokerages_string = ",".join(brokerages).upper()

        query_params = self.prepare_query_params(endpoint_name)

        if brokerages_string:
            query_params["brokerages"] = brokerages_string

        return self._make_request(endpoint_name, query_params=query_params)

    def get_currencies(self):
        """Get a list of currencies supported by SnapTrade"""
        endpoint_name = "currencies"
        query_params = self.prepare_query_params(endpoint_name)

        return self._make_request(endpoint_name, query_params=query_params)

    def get_all_currencies_exchange_rates(self):
        """Get a list of exchange rates for currencies pairs supported by SnapTrade"""
        endpoint_name = "currencies_rates"
        query_params = self.prepare_query_params(endpoint_name)

        return self._make_request(endpoint_name, query_params=query_params)

    def get_currency_pair_exchange_rate(self, src_currency_code, dst_currency_code):
        """Get the exchange rates for a currency pair supported by SnapTrade"""
        endpoint_name = "currency_pair_rate"
        query_params = self.prepare_query_params(endpoint_name)
        path_params = dict(currency_pair=f"{src_currency_code}-{dst_currency_code}")

        return self._make_request(endpoint_name, path_params=path_params, query_params=query_params)

    def search_symbols_by_name(self, substring):
        """Get details for symbols in SnapTrade servers by a string input"""
        endpoint_name = "symbol_search"
        query_params = self.prepare_query_params(endpoint_name)
        data = dict(substring=substring)

        return self._make_request(endpoint_name, data=data, query_params=query_params)

    def get_symbol_details_by_universal_symbol_id(self, symbol_id):
        """Get details for symbols in SnapTrade based on their universal symbol id"""
        endpoint_name = "symbol_by_id"
        query_params = self.prepare_query_params(endpoint_name)
        path_params = dict(symbol_id=symbol_id)

        return self._make_request(endpoint_name, path_params=path_params, query_params=query_params)

    def get_symbol_details_by_ticker(self, ticker):
        """Get details for symbols in SnapTrade based on their ticker"""
        endpoint_name = "symbol_by_ticker"
        query_params = self.prepare_query_params(endpoint_name)
        path_params = dict(ticker=ticker)

        return self._make_request(endpoint_name, path_params=path_params, query_params=query_params)

    def search_symbols_by_account(self, user_id, user_secret, account_id, substring):
        """Search universal symbol tickers based on their substring and account id"""
        endpoint_name = "account_symbols_search"

        initial_query_params = dict(
            userId=user_id,
            userSecret=user_secret,
        )

        query_params = self.prepare_query_params(endpoint_name, initial_query_params)
        path_params = dict(account_id=account_id)
        data = dict(substring=substring)

        return self._make_request(endpoint_name, data=data, path_params=path_params, query_params=query_params)

    def get_security_types(self):
        """Get a list of security types supported by SnapTrade"""

        endpoint_name = "security_types"
        query_params = self.prepare_query_params(endpoint_name)

        return self._make_request(endpoint_name, query_params=query_params)

    def get_partner_data(self):
        """Get data relevant to partner"""

        endpoint_name = "partner_details"
        query_params = self.prepare_query_params(endpoint_name)

        return self._make_request(endpoint_name, query_params=query_params)

    """
    Trading endpoints
    """

    def get_market_quotes(self, user_id, user_secret, account_id, symbols, search_by_ticker=False):
        """Gets market quotes of symbols using either their id or tickers"""

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

        return self._make_request(endpoint_name, path_params=path_params, query_params=query_params)

    def get_account_order_history(self, user_id, user_secret, account_id, state=None, days=None):
        """Gets the order history of an account"""
        endpoint_name = "account_orders_history"

        initial_query_params = dict(userId=user_id, userSecret=user_secret)

        if state:
            initial_query_params["state"] = state

        if days:
            initial_query_params["days"] = days

        query_params = self.prepare_query_params(endpoint_name, initial_params=initial_query_params)
        path_params = dict(account_id=account_id)

        return self._make_request(endpoint_name, path_params=path_params, query_params=query_params)

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
        """Gets the trade impact a trade has on an account"""
        endpoint_name = "trade_impact"

        initial_query_params = dict(userId=user_id, userSecret=user_secret)

        query_params = self.prepare_query_params(endpoint_name, initial_params=initial_query_params)

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

        return self._make_request(endpoint_name, data=trade_data, query_params=query_params)

    def place_order(self, user_id, user_secret, trade_id):
        """Places an order on a brokerage account"""
        endpoint_name = "place_order"

        initial_query_params = dict(userId=user_id, userSecret=user_secret)

        query_params = self.prepare_query_params(endpoint_name, initial_params=initial_query_params)

        path_params = dict(trade_id=trade_id)

        return self._make_request(endpoint_name, path_params=path_params, query_params=query_params)

    def cancel_order(self, user_id, user_secret, account_id, brokerage_order_id):
        """Cancels an existing order on a brokerage account"""
        endpoint_name = "cancel_order"

        initial_query_params = dict(userId=user_id, userSecret=user_secret)

        query_params = self.prepare_query_params(endpoint_name, initial_params=initial_query_params)

        path_params = dict(account_id=account_id)

        data = dict(brokerage_order_id=brokerage_order_id)

        return self._make_request(endpoint_name, path_params=path_params, query_params=query_params, data=data)

    def place_unvalidated_trade(        
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
        stop_price=None
    ):
        """Places a trade with no validation"""
        endpoint_name = "place_unvalidated_trade"

        initial_query_params = dict(userId=user_id, userSecret=user_secret)

        query_params = self.prepare_query_params(endpoint_name, initial_params=initial_query_params)

        
        if time_in_force.upper() == "DAY":
            time_in_force = time_in_force.title()
        else:
            time_in_force = time_in_force.upper()

        trade_data = {
            "account_id": account_id,
            "action": action.title(),
            "universal_symbol_id": universal_symbol_id,
            "order_type": order_type,
            "time_in_force": time_in_force,
            "units": units,
            "price": price,
            "stop": stop_price
        }

        return self._make_request(endpoint_name, data=trade_data, query_params=query_params)

    """
    SnapTrade Partners Brokerage API Credentials Endpoints
    """

    def get_all_brokerage_api_credentials(self):
        """Gets a list of all brokerage api credentials a SnapTrade partner has created"""
        endpoint_name = "api_credentials_list"
        query_params = self.prepare_query_params(endpoint_name)

        return self._make_request(endpoint_name, query_params=query_params)

    def create_brokerage_api_credentials(
        self,
        brokerage_authorization_type_id,
        brokerage_api_client_id=None,
        brokerage_api_client_secret=None,
        redirect_uri=None,
    ):
        """Creates a new Brokerage API Credential"""
        endpoint_name = "api_credentials_create"
        query_params = self.prepare_query_params(endpoint_name)

        data = {
            "brokerageAuthorizationTypeId": brokerage_authorization_type_id,
            "brokerageAPIClientId": brokerage_api_client_id,
            "brokerageAPIClientSecret": brokerage_api_client_secret,
            "redirectURI": redirect_uri,
        }

        return self._make_request(endpoint_name, data=data, query_params=query_params)

    def get_brokerage_api_credentials(self, credentials_id):
        """Gets the brokerage api credential by its id"""
        endpoint_name = "api_credentials"
        query_params = self.prepare_query_params(endpoint_name)

        path_params = dict(credentials_id=credentials_id)

        return self._make_request(endpoint_name, path_params=path_params, query_params=query_params)

    def update_brokerage_api_credentials(
        self, credentials_id, brokerage_api_client_id=None, brokerage_api_client_secret=None, redirect_uri=None
    ):
        """Updates an existing brokerage api credential"""
        endpoint_name = "api_credentials_update"
        query_params = self.prepare_query_params(endpoint_name)

        path_params = dict(credentials_id=credentials_id)

        data = {
            "brokerageAPIClientId": brokerage_api_client_id,
            "brokerageAPIClientSecret": brokerage_api_client_secret,
            "redirectURI": redirect_uri,
        }

        return self._make_request(endpoint_name, data=data, path_params=path_params, query_params=query_params)

    def delete_brokerage_api_credentials(self, credentials_id):
        """Deletes an existing brokerage api credential"""
        endpoint_name = "api_credentials_delete"
        query_params = self.prepare_query_params(endpoint_name)

        path_params = dict(credentials_id=credentials_id)

        return self._make_request(endpoint_name, path_params=path_params, query_params=query_params)

    def preview_option_trade(
        self,
        user_id: str,
        user_secret: str,
        account_id: str,
        option_symbol_id: str,
        order_type: str,
        time_in_force: str,
        action: str,
        units: int,
    ):
        """
        Executes a POST request to `v1/optionTrade/impact/` to ensure the validate of a proposed option trade.
        """
        endpoint_name = "preview_option_trade"
        initial_query_params = dict(userId=user_id, userSecret=user_secret)
        query_params = self.prepare_query_params(endpoint_name, initial_params=initial_query_params)
        path_params = dict()
        data = dict(
            account_id=account_id,
            option_symbol_id=option_symbol_id,
            order_type=order_type,
            time_in_force=time_in_force,
            action=action,
            units=units,
        )

        return self._make_request(endpoint_name, path_params=path_params, query_params=query_params, data=data)

    def execute_option_trade(self, user_id: str, user_secret: str, calculated_trade_id: str):
        """
        Executes an option trade, after previewing and confirming its validity with the `preview_option_trade` method above.
        Executes a POST request to `v1/optionTrade/%(uuid_pk)s/`.
        """
        endpoint_name = "execute_option_trade"
        initial_query_params = dict(userId=user_id, userSecret=user_secret)
        query_params = self.prepare_query_params(endpoint_name, initial_params=initial_query_params)
        path_params = dict(uuid_pk=calculated_trade_id)

        return self._make_request(endpoint_name, path_params=path_params, query_params=query_params)

    """
    Retrieve error logs
    """

    def retrieve_error_logs(self, user_id: str, userSecret: str):
        """Retrieve error logs associated with a particular user"""
        endpoint_name = "retrieve_error_logs"
        initial_query_params = dict(userId=user_id, userSecret=userSecret)

        query_params = self.prepare_query_params(endpoint_name, initial_params=initial_query_params)

        return self._make_request(endpoint_name, query_params=query_params, force_signature_auth=True)
