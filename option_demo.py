import logging

import requests
import snaptrade
from rich.logging import RichHandler

FORMAT = "%(message)s"
logging.basicConfig(level="INFO", format=FORMAT, datefmt="[%X]", handlers=[RichHandler()])

log = logging.getLogger("rich")
log.info("Welcome to the SnapTrade options trading demo!!")

import random
import string

from snaptrade.api_client import SnapTradeAPIClient


def generate_random_string(len: int = 10) -> str:
    """
    Generates a random string.
    Used to create a user id for a newly-created SnapTradeUser.
    Useful for this demo, since random user Ids allow you to easily
    create multiple users consecutively, without ID collisions.
    """
    output = ""
    for i in range(10):
        output += random.choice(string.ascii_letters)

    return output


CLIENT_ID = "DEMONM"
CONSUMER_KEY = ""


def register_new_snaptrade_user():
    client = SnapTradeAPIClient(CLIENT_ID, CONSUMER_KEY)
    client.base_url = "https://api.staging.passiv.com/api/"

    # Register a user
    user_id = generate_random_string()
    register_response = client.register_user(user_id)
    user_secret = register_response.get("userSecret")
    log.info(f"REGISTER USER: {register_response}")

    redirect_uri = client.get_user_login_redirect_uri(user_id, user_secret)["redirectURI"]
    print(f"Obtained redirect URI: {redirect_uri}")
    return user_id, user_secret


def demo_options_trade():

    # Initialize the API client, and verify the API is running correctly
    client = SnapTradeAPIClient(CLIENT_ID, CONSUMER_KEY)
    client.base_url = "https://api.staging.passiv.com/api/"
    api_status_response = client.api_status()
    log.info(f"API STATUS: {api_status_response}")

    # Register a user
    if False:
        user_id, user_secret = register_new_snaptrade_user()
        wait = input("Ready to proceed?\nPress Enter to continue.\n")
    else:
        user_id = "KkeUIMRWer"
        user_secret = "6f412f9d-c944-4f52-a970-7fa3419c3913"

    account_id = client.get_accounts(user_id, user_secret)[0]["id"]
    account_holdings = client.get_account_holdings(user_id, user_secret, account_id)

    option_position = account_holdings.get("option_positions")[0]
    option_symbol_id = option_position.get("symbol").get("option_symbol").get("id")
    order_type = "Market"
    time_in_force = "Day"
    action = "Buy"
    units = 1
    preview_trade_response = client.preview_option_trade(
        user_id, user_secret, account_id, option_symbol_id, order_type, time_in_force, action, units
    )
    log.info(f"Response from the Preview Trade endpoint: {preview_trade_response}")

    calculated_trade_id = preview_trade_response.get("id")

    execute_option_trade_response = client.execute_option_trade(user_id, user_secret, calculated_trade_id)
    log.info(f"Response from the Execute Trade endpoint: {execute_option_trade_response}")


if __name__ == "__main__":
    demo_options_trade()
