### 1) Get transaction history for a user

#### GET v1/activities

```
from snaptrade.api_client import SnapTradeAPIClient

client = SnapTradeAPIClient(clientID, consumerKey)

start_date = ""  # start_date should use the following format "YYYY-MM-DD"
end_date = ""    # end_date should use the following format "YYYY-MM-DD"

activities = client.get_activities(user_id, user_secret, start_date, end_date)
```

### 2) Get performance information (contributions, dividends, rate of return, etc) for a specific timeframe

#### GET v1/performance/custom

```
from snaptrade.api_client import SnapTradeAPIClient

client = SnapTradeAPIClient(clientID, consumerKey)

start_date = ""  # start_date should use the following format "YYYY-MM-DD"
end_date = ""  # end_date should use the following format "YYYY-MM-DD"
frequency = None # "weekly", "monthly", "quarterly" or "yearly"
account_ids = None  # Optional comma seperated list of account IDs used to filter the request on specific accounts

performance_info = client.get_performance_custom(user_id, user_secret, start_date, end_date, frequency, account_ids)
```
