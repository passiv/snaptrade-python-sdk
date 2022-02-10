from snaptrade.api_client import SnapTradeAPIClient
from snaptrade.models import (
    APIStatus,
    Account,
    Brokerage,
    User,
    Currency,
    ExchangeRate,
    UniversalSymbol,
)


class APIManager:
    def __init__(self, client_id, consumer_key, user_id=None, user_secret=None):
        self.client_id = client_id
        self.consumer_key = consumer_key
        self.user_id = user_id
        self.user_secret = user_secret

        self.api_client = SnapTradeAPIClient(
            self.client_id, self.consumer_key, return_response_as_dict=False
        )

    """Get status for api server"""

    def get_api_status(self):
        status = self.api_client.api_status()

        if status.class_name == "ErrorMessage":
            return status

        return APIStatus(status)

    """Methods in this section deals with user registration, auth & deletion"""

    def register_user(self):
        user_details = self.api_client.register_user(self.user_id)

        if user_details.class_name == "ErrorMessage":
            return user_details

        user = User.init_from_user_details(user_details, namespace=True)

        self.user_secret = user.user_secret

        return user

    def delete_user(self):
        user_delete_details = self.api_client.delete_user(self.user_id)

        if user_delete_details.class_name == "ErrorMessage":
            return user_delete_details

        return user_delete_details

    def get_user_login_redirect_uri(self):
        redirect_uri = self.api_client.get_user_login_redirect_uri(
            self.user_id, self.user_secret
        )

        if redirect_uri.class_name == "ErrorMessage":
            return redirect_uri

        return redirect_uri.redirectURI

    """Methods in this section deals with accounts details, account holdings and account activities"""

    def get_accounts(self):
        raw_accounts = self.api_client.get_accounts(self.user_id, self.user_secret)

        if raw_accounts.class_name == "ErrorMessage":
            return raw_accounts

        raw_accounts_list = raw_accounts.data
        accounts = Account.init_from_raw_data(raw_accounts_list)

        return accounts

    """Methods in this sections deals with obtaining reference data"""

    def get_brokerages(self):
        raw_brokerages = self.api_client.get_brokerages()

        if raw_brokerages.class_name == "ErrorMessage":
            return raw_brokerages

        raw_brokerages_list = raw_brokerages.data
        brokerages = Brokerage.init_from_raw_data(raw_brokerages_list)

        return brokerages

    def get_currencies(self):
        raw_currencies = self.api_client.get_currencies()

        if raw_currencies.class_name == "ErrorMessage":
            return raw_currencies

        raw_currencies_list = raw_currencies.data
        currencies = Currency.init_from_raw_data(raw_currencies_list)

        return currencies

    def get_currencies_exchange_rates(self):
        raw_exchange_rates = self.api_client.get_all_currencies_exchange_rates()

        if raw_exchange_rates.class_name == "ErrorMessage":
            return raw_exchange_rates

        raw_currencies_list = raw_exchange_rates.data
        exchange_rates = ExchangeRate.init_from_raw_data(raw_currencies_list)

        return exchange_rates

    def get_currency_pair_exchange_rates(self, src_currency_code, dst_currency_code):
        raw_exchange_rate = self.api_client.get_currency_pair_exchange_rate(
            src_currency_code, dst_currency_code
        )

        if raw_exchange_rate.class_name == "ErrorMessage":
            return raw_exchange_rate

        exchange_rate = ExchangeRate.init_from_raw_data(raw_exchange_rate)

        return exchange_rate

    def search_symbols_by_name(self, substring):
        raw_symbols = self.api_client.search_symbols_by_name(substring)

        if raw_symbols.class_name == "ErrorMessage":
            return raw_symbols

        raw_symbols_list = raw_symbols.data

        symbols = UniversalSymbol.init_from_raw_data(raw_symbols_list)

        return symbols

    def get_symbol_details_by_universal_symbol_id(self, symbol_id):
        raw_symbol = self.api_client.get_symbol_details_by_universal_symbol_id(
            symbol_id
        )

        if raw_symbol.class_name == "ErrorMessage":
            return raw_symbol

        symbol = UniversalSymbol.init_from_raw_data(raw_symbol)

        return symbol

    def get_symbol_details_by_ticker(self, ticker):
        raw_symbol = self.api_client.get_symbol_details_by_ticker(ticker)

        if raw_symbol.class_name == "ErrorMessage":
            return raw_symbol

        symbol = UniversalSymbol.init_from_raw_data(raw_symbol)

        return symbol

    """Methods in this section deals with trading endpoints"""

    """Methods in this section deals with trading endpoints"""
