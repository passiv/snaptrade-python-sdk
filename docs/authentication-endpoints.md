### 1) Creating a new user 

#### POST v1/snapTrade/registerUser

```
from snaptrade.api_client import SnapTradeAPIClient

client = SnapTradeAPIClient(clientID, consumerKey)

register_response = client.register_user(user_id)

user_secret = register_response.get("userSecret") 
```

### 2) Generate a redirectURI to SnapTrade Connection Portal 

#### POST v1/snapTrade/login

```
from snaptrade.api_client import SnapTradeAPIClient

client = SnapTradeAPIClient(clientID, consumerKey)

redirect_uri_response = client.get_user_login_redirect_uri(user_id, user_secret)

redirect_uri = redirect_uri_response.get("redirectURI")
```

### 3) Delete an existing user

#### POST v1/snapTrade/deleteUser

```
from snaptrade.api_client import SnapTradeAPIClient

client = SnapTradeAPIClient(clientID, consumerKey)

deleted_response = client.delete_user(user_id)
```
