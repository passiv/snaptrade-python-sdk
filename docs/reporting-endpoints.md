### 1) Get transaction history for a user

#### GET v1/activities

```
from snaptrade.api_client import SnapTradeAPIClient

client = SnapTradeAPIClient(clientID, consumerKey)

start_date = "2022-01-01"  # Optional: start_date should use the following format "YYYY-MM-DD"
end_date = "2022-01-31"    # Optional: end_date should use the following format "YYYY-MM-DD"
account_ids = ["ddb9e8e5-4b4d-4adb-9b57-6114c467069e,cb174d1f-443c-441c-8c6f-6e31e95da699"] # Optional: List of account ids

activities = client.get_activities(user_id, user_secret, start_date, end_date, accountIDs=account_ids)
```


### 2) Get custom performance of selected accounts

#### GET v1/performance/custom

```
from snaptrade.api_client import SnapTradeAPIClient

client = SnapTradeAPIClient(clientID, consumerKey)

start_date = "2022-01-01"
end_date = "2022-08-31"
account_ids = ["ddb9e8e5-4b4d-4adb-9b57-6114c467069e,cb174d1f-443c-441c-8c6f-6e31e95da699"] # Optional: List of account ids

activities = client.get_performance_custom(user_id, user_secret, start_date, end_date, accountIDs=account_ids)
```
