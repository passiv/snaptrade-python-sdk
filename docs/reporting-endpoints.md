### 1) Get transaction history for a user

#### GET v1/activities

```
from snaptrade.snaptrade_api_client import SnapTradeAPIClient

client = SnapTradeAPIClient(clientID, consumerKey)

start_date = ""  # start_date should use the following format "YYYY-MM-DD"
end_date = ""    # end_date should use the following format "YYYY-MM-DD"


activities = client.get_activities(user_id, user_secret, start_date, end_date)
```