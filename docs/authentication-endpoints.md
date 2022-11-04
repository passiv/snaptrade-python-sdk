### 1) Creating a new user

#### POST v1/snapTrade/registerUser

```
from snaptrade.api_client import SnapTradeAPIClient

client = SnapTradeAPIClient(clientID, consumerKey)

# rsa_public_key is nullable, if it is not required for the user
register_response = client.register_user(user_id, rsa_public_key)

user_secret = register_response.get("userSecret")
```

### 2) Generate a redirectURI to SnapTrade Connection Portal

#### POST v1/snapTrade/login

```
from snaptrade.api_client import SnapTradeAPIClient

client = SnapTradeAPIClient(clientID, consumerKey)

broker = ""    # Optional: broker slug to connect directly to broker
immediate_redirect = False    # Optional: boolean to redirect straight to redirect uri instead of going to Snaptrade connection portal
custom_redirect = ""    # Optional: redirct uri 
reconnect = ""   # Optional: Brokerage authorization id to reconnect
connection_type = ""   # Optional: Connection type code (read/trade)

redirect_uri_response = client.get_user_login_redirect_uri(user_id, user_secret, broker, immediate_redirect, custom_redirect, reconnect)

redirect_uri = redirect_uri_response.get("redirectURI")
```

### 3) Delete an existing user

#### POST v1/snapTrade/deleteUser

```
from snaptrade.api_client import SnapTradeAPIClient

client = SnapTradeAPIClient(clientID, consumerKey)

deleted_response = client.delete_user(user_id)
```

### 4) Get an encrypted JWT for the user

#### GET v1/snapTrade/encryptedJWT

```
from snaptrade.api_client import SnapTradeAPIClient

client = SnapTradeAPIClient(clientID, consumerKey)

encrypted_jwt = client.get_encrypted_jwt(user_id, user_secret)
```

### 5) Gets a list of users registered by partner
#### GET v1/snapTrade/listUsers

```
from snaptrade.api_client import SnapTradeAPIClient

client = SnapTradeAPIClient(clientID, consumerKey)

registered_users = client.get_registered_users()
```
