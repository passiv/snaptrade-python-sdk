import logging

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

redirect_uri = client.get_user_login_redirect_uri(user_id, user_secret)

account_holdings_data = client.get_all_holdings(user_id, user_secret)

client.delete_user(user_id)

"""

logger = logging.getLogger("django")

from snaptrade.api_client.snaptrade_api_client import SnapTradeAPIClient


def print_welcome():
    logger.info(
        "Welcome to SnapTrade Python SDK Demo \n"
        "You can use this code as a quick test to ensure that everything is working as intended."
    )


def get_client_credentials():
    logger.info("To help you get started, please enter the following information")
    client_id = input("Client ID: ")
    consumer_key = input("Consumer Key: ")

    return client_id, consumer_key


def user_auth_option():
    logger.info(
        "Choose an action by entering a number below:\n"
        "1) Create new user \n"
        "2) Login with existing user \n"
        "3) Delete Existing Use \n"
        "Press [Enter] to quit"
    )

    option = input("Enter option: ")

    return option


def print_account_holdings_data(accounts_holdings_data):
    if not accounts_holdings_data:
        logger.info(">>> There is account summary to show. Please add a brokerage connection to get holdings data.")
    for account_holdings_data in accounts_holdings_data:
        account_brokerage = account_holdings_data["account"].get("brokerage")
        account_name = account_holdings_data["account"].get("name")
        account_number = account_holdings_data["account"].get("number")

        balances_data = account_holdings_data.get("balances")
        positions_data = account_holdings_data.get("positions")

        logger.info(f"Account: {account_brokerage} - {account_name}: {account_number} \n" "    Balances:")
        if not balances_data:
            logger.info("      No balance data to display \n")
        else:
            for balance_data in balances_data:
                logger.info(f"      ${balance_data.get('cash')} {balance_data['currency'].get('code')} \n")

        logger.info("    Positions:")
        if not positions_data:
            logger.info("    No positions data to display \n")
        else:
            logger.info(f"      {'Ticker'.ljust(15)} {'Units'.ljust(15)} {'Price'.ljust(15)} \n ")
            logger.info("      ---------------------------------------------")
            for position_data in positions_data:
                ticker = position_data["symbol"].get("symbol")
                units = position_data.get("units")
                price = position_data.get("price")
                currency = position_data["symbol"]["currency"].get("code")
                logger.info(f"      {str(ticker).ljust(15)} {str(units).ljust(15)} {str(price).ljust(8)} {currency}")


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
                logger.info("Please enter the following information: \n")
                user_id = input("UserID: ")

                # Makes request to `api/v1/snapTrade/registerUser` endpoint
                registration_response = client.register_user(user_id)
                user_secret = registration_response.get("userSecret")

                if user_secret:
                    logger.info("Please store the following user secret for future reference:")
                    logger.info(f"{user_secret}")
                    input("Press [enter] to continue")
                elif registration_response.get("code") == 1010:
                    logger.info(f"{user_id} already exist. Please enter a user secret. \n")
                    user_secret = input("User Secret (Press [enter] to quit): ")
                else:
                    logger.info(
                        f"Something went wrong. We were unable to create a new user. Please ensure that clientId and consumer_key are correct."
                    )
                if not user_secret:
                    return 0
                break
            elif auth_option == "2":
                logger.info("Please enter the following information:")
                user_id = input("UserID: ")
                user_secret = input("User Secret (Press [enter] to quit): ")
                if not user_secret:
                    return 0
                break
            elif auth_option == "3":
                logger.info("Please enter the userID of the user you would like to delete:")
                user_id = input("UserID: ")

                # Makes request to `api/v1/snapTrade/deleteUser` endpoint
                delete_response = client.delete_user(user_id)

                if delete_response.get("status") == "deleted":
                    logger.info(f"{user_id} has been successfully delete \n")
                elif (
                    delete_response.get("detail") == "Invalid userID was provided"
                    or delete_response.get("code") == "1083"
                ):
                    logger.info(
                        f"Failed to delete user with userID {user_id}. User might already have been deleted previously or was never created"
                    )
            else:
                logger.info(
                    "Thank you for trying our SnapTrade demo! Please reach out if you have any questions or comments."
                )
                return 0

        # Make request to `api/v1/snapTrade/login` endpoint
        login_redirect_uri = client.get_user_login_redirect_uri(user_id, user_secret)

        redirect_url = login_redirect_uri.get("redirectURI")

        if redirect_url:
            logger.info(f"Open this link in your browser to add a brokerage connection to SnapTrade:")
            logger.info(f"{redirect_url} \n")
            input("Press [enter] when you're ready to continue: ")
        else:
            logger.info(
                "Something went wrong. Unable to get redirect uri. Please check that the `clientId`, `consumer_keys`, `user_id` and `user_secret` provided was correct."
            )
            logger.info("Exiting script...")
            return 0

        logger.info("Please wait a moment while we retrieve your account information:...")

        account_holdings_data = client.get_all_holdings(user_id, user_secret)

        print_account_holdings_data(account_holdings_data)

        logger.info("Thank you for trying our SnapTrade demo! Please reach out if you have any questions or comments.")

    else:
        logger.info("We were unable to connect to the api at this time. Please contact support for help")


if __name__ == "__main__":
    main()
