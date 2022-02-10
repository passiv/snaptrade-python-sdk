from snaptrade.managers import BaseManager
from snaptrade.models import User


class UserManager(BaseManager):
    def __init__(self, client_id, consumer_key, user_id=None, user_secret=None):
        super().__init__(client_id, consumer_key, user_id, user_secret, return_response_as_dict=False)

    def register_user(self):
        user_details = self.api_client.register_user(self.user_id)

        if user_details.class_name == "ErrorMessage":
            return user_details

        user = User.init_from_user_details(user_details, namespace=True)

        self.user_secret = user.user_secret

        return user

    def delete_user(self):
        user_delete_details = self.api_client.delete_user(self.user_id)

        if user_delete_details.class_name == "ErrorMessage":
            return user_delete_details

        return user_delete_details

    def get_user_login_redirect_uri(self):
        redirect_uri = self.api_client.get_user_login_redirect_uri(self.user_id, self.user_secret)

        if redirect_uri.class_name == "ErrorMessage":
            return redirect_uri

        return redirect_uri.redirectURI