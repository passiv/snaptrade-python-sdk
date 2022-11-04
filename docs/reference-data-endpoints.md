### 1) Get list of all supported brokerages

#### GET v1/brokerages
```
from snaptrade.api_client import SnapTradeAPIClient

client = SnapTradeAPIClient(clientID, consumerKey)

brokerages = client.get_brokerages()
```


### 2) Get list of all supported currencies

#### GET v1/currencies
```
from snaptrade.api_client import SnapTradeAPIClient

client = SnapTradeAPIClient(clientID, consumerKey)

currencies = client.get_currencies()
```

### 3) Get exchange rates for all supported currencies

#### GET v1/currencies/rates
```
from snaptrade.api_client import SnapTradeAPIClient

client = SnapTradeAPIClient(clientID, consumerKey)

currencies = client.get_all_currencies_exchange_rates()
```

### 4) Get exchange rate for a currency pair

#### GET v1/currencies/{currencyPair}

eg. If converting CAD into USD `src_currency_code=CAD` and `dst_currency_code=USD`
```
from snaptrade.api_client import SnapTradeAPIClient

client = SnapTradeAPIClient(clientID, consumerKey)

src_currency_code = ""  # Base Currency Code
dst_currency_code = ""  # Currency to convert to

currencies = client.get_currency_pair_exchange_rate(src_currency_code, dst_currency_code)
```

### 5) Search symbols with provided string

#### POST v1/symbols

```
from snaptrade.api_client import SnapTradeAPIClient

client = SnapTradeAPIClient(clientID, consumerKey)

substring = "" # Search for symbol which matches this substring
symbols = client.search_symbols_by_name(substring)
```


### 6) Get symbol details using symbol id

#### GET v1/symbols/{symbolId}

```
from snaptrade.api_client import SnapTradeAPIClient

client = SnapTradeAPIClient(clientID, consumerKey)

symbol_id = ""  # symbol_id should be a UUID
symbols = client.get_symbol_details_by_universal_symbol_id(symbol_id)
```

### 6) Get symbol details using symbol ticker

#### GET v1/symbols/{ticker}

```
from snaptrade.api_client import SnapTradeAPIClient

client = SnapTradeAPIClient(clientID, consumerKey)

symbol_ticker = ""  # symbol ticker to search
symbols = client.get_symbol_details_by_ticker(symbol_ticker)
```

### 7) Gets a list of security types

#### GET v1/securityTypes

```
from snaptrade.api_client import SnapTradeAPIClient

client = SnapTradeAPIClient(clientID, consumerKey)

security_types = client.get_security_types(symbol_ticker)
```

### 8) Get a list of brokerage authorization types

#### GET v1/brokerageAuthorizations

```
from snaptrade.api_client import SnapTradeAPIClient

client = SnapTradeAPIClient(clientID, consumerKey)

brokerages = []  # A list of brokerage slugs. Usually the name of the brokerage in capital letters

brokerage_authorization_types = client.get_brokerage_authorization_types(brokerages)
```

### 9) Get metadata for partner

#### GET v1/snapTrade/partners

```
from snaptrade.api_client import SnapTradeAPIClient

client = SnapTradeAPIClient(clientID, consumerKey)

partner_data  = client.get_partner_data()
```
