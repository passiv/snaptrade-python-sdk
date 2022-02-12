"""
TL/DR: Summary of methods use in script to make requests to SnapTrade API

1) Initialize SnapTrade API client
2) Checks SnapTrade api server is online
3) Register a user
4) Gets redirect uri to connect brokerage to SnapTrade
5) Gets account holdings data
6) Delete a user and all other data linked to the user


from .snaptrade.api_client.snaptrade_api_client import SnapTradeAPIClient


client = SnapTradeAPIClient(clientId, consumer_key)

api_status = client.api_status()

registered_user_data = client.register_user(user_id)

redirect_uri = client.get_user_login_redirect_uri

account_holdings_data = client.get_all_holdings(user_id, user_secret)

client.delete_user()

"""


from snaptrade.api_client.snaptrade_api_client import SnapTradeAPIClient


def print_welcome():
    print("Welcome to SnapTrade Python SDK Demo")
    print(
        "You can use this code as a quick test to ensure that everything is working as intended."
    )
    print("")


def get_client_credentials():
    print("To help you get started, please enter the following information")
    client_id = input("Client ID: ")
    consumer_key = input("Consumer Key: ")
    print("")

    return client_id, consumer_key


def user_auth_option():
    print("Choose an action by entering a number below:")
    print("1) Create new user")
    print("2) Login with existing user")
    print("3) Delete Existing User")
    print("Press [Enter] to quit")
    print("")
    option = input("Enter option: ")
    print("")

    return option


def print_account_holdings_data(accounts_holdings_data):
    if not accounts_holdings_data:
        print("")
        print(
            ">>> There is account summary to show. Please add a brokerage connection to get holdings data."
        )
    print("")
    for account_holdings_data in accounts_holdings_data:
        account_brokerage = account_holdings_data["account"].get("brokerage")
        account_name = account_holdings_data["account"].get("name")
        account_number = account_holdings_data["account"].get("number")

        balances_data = account_holdings_data.get("balances")
        positions_data = account_holdings_data.get("positions")

        print(f"Account: {account_brokerage} - {account_name}: {account_number}")
        print("    Balances:")
        if not balances_data:
            print("      No balance data to display")
        else:
            for balance_data in balances_data:
                print(
                    f"      ${balance_data.get('cash')} {balance_data['currency'].get('code')}"
                )

        print("")

        print("    Positions:")
        if not positions_data:
            print("    No positions data to display")
        else:
            print(f"      {'Ticker'.ljust(15)} {'Units'.ljust(15)} {'Price'.ljust(15)}")
            print("      ---------------------------------------------")
            for position_data in positions_data:
                ticker = position_data["symbol"].get("symbol")
                units = position_data.get("units")
                price = position_data.get("price")
                currency = position_data["symbol"]["currency"].get("code")
                print(
                    f"      {str(ticker).ljust(15)} {str(units).ljust(15)} {str(price).ljust(8)} {currency}"
                )

        print("")
        print("")


def main():
    print_welcome()
    client_id, consumer_key = get_client_credentials()

    # Initialize SnapTradeAPIClient
    client = SnapTradeAPIClient(client_id, consumer_key)

    # Makes request to `api/v1/` endpoint
    api_online = client.api_status().get("online")

    if api_online:
        user_secret = ""

        while True:
            auth_option = user_auth_option()
            if auth_option == "1":
                print("Please enter the following information:")
                user_id = input("UserID: ")

                # Makes request to `api/v1/snapTrade/registerUser` endpoint
                registration_response = client.register_user(user_id)
                user_secret = registration_response.get("userSecret")

                if user_secret:
                    print("")
                    print(
                        "Please store the following user secret for future reference:"
                    )
                    print(f"{user_secret}")
                    print("")
                    input("Press [enter] to continue")
                elif registration_response.get("code") == 1010:
                    print(f"{user_id} already exist. Please enter a user secret.")
                    user_secret = input("User Secret (Press [enter] to quit): ")
                    print("")
                else:
                    print(
                        f"Something went wrong. We were unable to create a new user. Please ensure that clientId and consumer_key are correct."
                    )
                if not user_secret:
                    return 0
                break
            elif auth_option == "2":
                print("Please enter the following information:")
                user_id = input("UserID: ")
                user_secret = input("User Secret (Press [enter] to quit): ")
                print("")
                if not user_secret:
                    return 0
                break
            elif auth_option == "3":
                print("Please enter the userID of the user you would like to delete:")
                user_id = input("UserID: ")

                # Makes request to `api/v1/snapTrade/deleteUser` endpoint
                delete_response = client.delete_user(user_id)

                if delete_response.get("status") == "deleted":
                    print("")
                    print(f"{user_id} has been successfully delete")
                    print("")
                elif (
                    delete_response.get("detail") == "Invalid userID was provided"
                    or delete_response.get("code") == "1083"
                ):
                    print("")
                    print(
                        f"Failed to delete user with userID {user_id}. User might already have been deleted previously or was never created"
                    )
                    print("")
            else:
                print(
                    "Thank you for trying our SnapTrade demo! Please reach out if you have any questions or comments."
                )
                return 0

        # Make request to `api/v1/snapTrade/login` endpoint
        login_redirect_uri = client.get_user_login_redirect_uri(user_id, user_secret)

        redirect_url = login_redirect_uri.get("redirectURI")

        if redirect_url:
            print("")
            print("")
            print(
                f"Open this link in your browser to add a brokerage connection to SnapTrade:"
            )
            print("")
            print(f"{redirect_url}")
            print("")
            input("Press [enter] when you're ready to continue: ")
            print("")
        else:
            print(
                "Something went wrong. Unable to get redirect uri. Please check that the `clientId`, `consumer_keys`, `user_id` and `user_secret` provided was correct."
            )
            print("Exiting script...")
            print("")
            return 0

        print("")
        print("Please wait a moment while we retrieve your account information:...")
        print("")

        account_holdings_data = client.get_all_holdings(user_id, user_secret)

        print_account_holdings_data(account_holdings_data)

        print("")
        print(
            "Thank you for trying our SnapTrade demo! Please reach out if you have any questions or comments."
        )
        print("")

    else:
        print(
            "We were unable to connect to the api at this time. Please contact support for help"
        )
        print("")


if __name__ == "__main__":
    main()
