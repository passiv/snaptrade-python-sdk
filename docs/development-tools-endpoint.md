### 1) Gets list of all brokerage api credentials linked to SnapTrade partner

#### GET v1/snapTrade/apiCredentials
```
from snaptrade.api_client import SnapTradeAPIClient

client = SnapTradeAPIClient(clientID, consumerKey)

brokerages = client.get_all_brokerage_api_credentials()
```

### 2) Creates a new brokerage api credential for SnapTrade partner

#### POST v1/snapTrade/apiCredentials
```
from snaptrade.api_client import SnapTradeAPIClient

client = SnapTradeAPIClient(clientID, consumerKey)

brokerage_authorization_type_id =      # Brokerage authorization type id (obtained from v1/brokerages
brokerage_api_client_id=None
brokerage_api_client_secret=None
redirect_uri=None

brokerages = client.create_brokerage_api_credentials(brokerage_authorization_type_id, brokerage_api_client_id, brokerage_api_client_secret, redirect_uri)
```

### 3) Gets a brokerage api credential obj

#### GET v1/snapTrade/apiCredentials/{apiClientId}
```
from snaptrade.api_client import SnapTradeAPIClient

client = SnapTradeAPIClient(clientID, consumerKey)

api_credentials_id =    # Id of api credential object

brokerages = client.get_brokerage_api_credentials(api_credentials_id)
```

### 4) Updates a brokerage api credential obj

#### POST v1/snapTrade/apiCredentials/{apiClientId}
```
from snaptrade.api_client import SnapTradeAPIClient

client = SnapTradeAPIClient(clientID, consumerKey)

api_credentials_id =    # Id of api credential object

brokerage_api_client_id=None
brokerage_api_client_secret=None
redirect_uri=None

brokerages = client.update_brokerage_api_credentials(brokerage_api_client_id, brokerage_api_client_secret, redirect_uri)
```

### 5) Deletes a brokerage api credential obj

#### Delete v1/snapTrade/apiCredentials/{apiClientId}
```
from snaptrade.api_client import SnapTradeAPIClient

client = SnapTradeAPIClient(clientID, consumerKey)

api_credentials_id =    # Id of api credential object

brokerages = client.delete_brokerage_api_credentials(api_credentials_id)
```
