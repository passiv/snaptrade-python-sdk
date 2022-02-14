### 1) Get all brokerage connections for the user

#### GET v1/authorizations

```
from snaptrade.snaptrade_api_client import SnapTradeAPIClient

client = SnapTradeAPIClient(clientID, consumerKey)

connections = client.get_brokerage_connections(user_id, user_secret)
```

### 2) Get detail of a brokerage connection

#### GET v1/authorizations/{authorizationId}
```
from snaptrade.snaptrade_api_client import SnapTradeAPIClient

client = SnapTradeAPIClient(clientID, consumerKey)

connections = client.get_brokerage_connection_by_id(user_id, user_secret, brokerage_connection_id)
```

### 3) Delete of a brokerage connection

#### DELETE v1/authorizations/{authorizationId}
```
from snaptrade.snaptrade_api_client import SnapTradeAPIClient

client = SnapTradeAPIClient(clientID, consumerKey)

connections = client.get_brokerage_connection_by_id(user_id, user_secret, brokerage_connection_id)
```
