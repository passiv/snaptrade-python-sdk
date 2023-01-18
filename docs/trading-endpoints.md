### 1) Get quotes of symbols

#### GET v1/accounts/{accountId}/quotes
```
from snaptrade.api_client import SnapTradeAPIClient

client = SnapTradeAPIClient(clientID, consumerKey)

symbols = []  # Must be a list of symbol id or a list of symbol tickers
search_by_ticker = True  # Set to True if symbols array is a list of tickers, False if it's a list of ids

quotes = client.get_market_quotes(user_id, user_secret, symbols, search_by_ticker)
```

### 2) Get history of orders placed in accounts

#### GET v1/accounts/{accountId}/orders
```
from snaptrade.api_client import SnapTradeAPIClient

client = SnapTradeAPIClient(clientID, consumerKey)

state = ""  # Optional: One of "executed", "open", "all"
days = ""  # Optional: Filter query for records since X days from today

quotes = client.get_account_order_history(user_id, user_secret, account_id, state, days)
```

### 3) Get impact of trade on account

#### GET v1/trade/impact

* Note: Endpoint needs to be called before placing an order to get id
```
from snaptrade.api_client import SnapTradeAPIClient

client = SnapTradeAPIClient(clientID, consumerKey)

action = ""  # BUY|SELL
universal_symbol_id = ""  # Id of symbol object, should be a UUID
order_type = ""   # Limit|Market
time_in_force = "" # Day|FOK
units = ""  # Must be a positive whole number
price = ""  # Required if using Limit order, must be positive decimal numbers

trade_impact = client.get_trade_impact(
        user_id,
        user_secret,
        account_id,
        action,
        universal_symbol_id,
        order_type,
        time_in_force,
        units,
        price=None,
    )
```

### 4) Place an order

#### POST v1/trade/{tradeId}
```
from snaptrade.api_client import SnapTradeAPIClient

client = SnapTradeAPIClient(clientID, consumerKey)

trade_id = ""  # id obtained when getting trade impact in step #3

order_response = client.place_order(user_id, user_secret, trade_id)
```

### 5) Cancel an order

#### POST v1/accounts/{accountId}/orders/cancel
```
from snaptrade.api_client import SnapTradeAPIClient

client = SnapTradeAPIClient(clientID, consumerKey)

brokerage_order_id = ""  # Order id as returned by broker. Obtained in either step #2 or #4

order_response = client.cancel_order(user_id, user_secret, account_id, brokerage_order_id)
```

### 6) Place a trade with NO validation.

#### GET v1/trade/place

```
from snaptrade.api_client import SnapTradeAPIClient

client = SnapTradeAPIClient(clientID, consumerKey)

action = ""  # BUY|SELL
universal_symbol_id = ""  # Id of symbol object, should be a UUID
order_type = ""   # Limit|Market
time_in_force = "" # Day|FOK|GTC
units = ""  # Must be a positive whole number
price = ""  # Required if using Limit order, must be positive decimal numbers
stop = "" # Required if using a stop price

trade_impact = client.place_unvalidated_trade(
        user_id,
        user_secret,
        account_id,
        action,
        universal_symbol_id,
        order_type,
        time_in_force,
        units,
        price=price,
        stop=stop
    )
```