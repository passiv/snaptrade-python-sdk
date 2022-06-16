### 1) Get all investment accounts for the user

#### GET v1/accounts

```
from snaptrade.api_client import SnapTradeAPIClient

client = SnapTradeAPIClient(clientID, consumerKey)

accounts = client.get_accounts(user_id, user_secret)
```

### 2) Get detail of an individual investment account

#### GET v1/accounts/{accountId}

```
from snaptrade.api_client import SnapTradeAPIClient

client = SnapTradeAPIClient(clientID, consumerKey)

account = client.get_account_by_id(user_id, user_secret, account_id)
```

### 3) Get balances of an investment account

#### GET v1/accounts/{accountId}/balances

```
from snaptrade.api_client import SnapTradeAPIClient

client = SnapTradeAPIClient(clientID, consumerKey)

account_balances = client.get_account_balances(user_id, user_secret)
```

### 4) Get positions of an investment account

#### GET v1/accounts/{accountId}/positions

```
from snaptrade.api_client import SnapTradeAPIClient

client = SnapTradeAPIClient(clientID, consumerKey)

account_positions = client.get_account_positions(user_id, user_secret)
```

### 5) Get all balances and holdings data for an investment account

#### GET v1/accounts/{accountId}/holdings

```
from snaptrade.api_client import SnapTradeAPIClient

client = SnapTradeAPIClient(clientID, consumerKey)

account_holdings = client.get_account_holdings(user_id, user_secret, account_id)
```

### 6) Get all balances and holdings data for all accounts

#### GET v1/holdings

```
from snaptrade.api_client import SnapTradeAPIClient

client = SnapTradeAPIClient(clientID, consumerKey, brokerage_authorization_ids=None, account_numbers=None)

# brokerage_authorization_ids and account_numbers are optional, but expects a list if used.

account_holdings = client.get_all_holdings(user_id, user_secret, ["36ccb6ce-f71a-492c-99c5-38c4076bd6d1"], [2419011])
```
