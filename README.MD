# SnapTrade-Python
A SnapTrade python client library to help you make requests to the [SnapTrade API][1] endpoints more easily.


If you need help or have any questions, send us an email at [api@snaptrade.com][contact].

---
## Requirements and Installation 
### Python version requirements
* Python 3.6 or later

### Installation
```
pip install snaptrade
```
* It is recommended that you install this library on a virtual environment. You can find out more about this in the following link: 
[Installing using pip and virtual environments]

---
## SnapTradeAPIClient
Before getting started, you will need a **clientID** and a **consumerKey**. If you don't have one, please send us an email 
to get a new one. 

### Why use SnapTradeAPIClient?
1) The client uses the clientID and consumerKey that you pass in to sign a request. This ensures that all requests made to the API server are signed and authenticated correctly.
2) The client ensures that any data passed in through the path params, query params or request body are formatted correctly.
3) The client formats the API responses and returns a dictionary of the data returned.

### How to use SnapTradeAPIClient?
The code block belows shows you to initialize a SnapTradeAPIClient and how to make requests with it.

```
"""
Your consumerKey should always remain a secret! Never hard code it! 
""" 

from snaptrade.snaptrade_api_client import SnapTradeAPIClient
 
# 1) Initialize a client with your clientID and consumerKey. 
client = SnapTradeAPIClient(clientID, consumerKey)

# 2) Check that the client is able to make a request to the API server. 
api_status_response = client.api_status()
print(api_status_response)

# 3) Create a new user on SnapTrade 
user_id = "userIDProvidedByPartner"
register_response = client.register_user(user_id)

# Note: A user secret is only generated once. It's required to access
# resources for certain endpoints. 

user_secret = register_response.get("userSecret") 

# 4) Get a redirect URI. Users will need this to connect 
# their brokerage to the SnapTrade server.

redirect_uri = client.get_user_login_redirect_uri(user_id, user_secret).get("redirectURI")

# 5) Obtaining account holdings data

holdings = client.get_all_holdings(user_id, user_secret)

# 6) Deleting a user
deleted_response = client.delete_user(user_id)
```

Check out the documentation below for making requests to other SnapTrade API endpoints using this client
* [Account Information Endpoints]
* [Authentication Endpoints]
* [Connections Endpoints]
* [Reference Data Endpoints]
* [Reporting Endpoints]
* [Trading Endpoints]

---
## License & copyrights

Licensed under [Apache License 2.0][2]. 

[1]: https://docs.snaptrade.com/reference/getting-started
[contact]: mailto:api@snaptrade.com
[Account Information Endpoints]: docs/account-information-endpoints.md
[Authentication Endpoints]: docs/authentication-endpoints.md
[Connections Endpoints]: docs/connections-endpoints.md
[Reference Data Endpoints]: docs/reference-data-endpoints.md
[Reporting Endpoints]: docs/reporting-endpoints.md
[Trading Endpoints]: docs/trading-endpoints.md
[Installing using pip and virtual environments]: https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/
[2]: LICENSE