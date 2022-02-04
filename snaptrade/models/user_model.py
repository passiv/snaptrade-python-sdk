from snaptrade.models.base_model import BaseModel

class User(BaseModel):
    def __init__(self, user_id, user_secret=None):
        self.user_id = user_id
        self.user_secret = user_secret

    _gen_str_params = ("user_id",)

    @classmethod
    def init_from_user_details(cls, user_details, namespace=False):
        if namespace:
            return cls(user_details.userId, user_details.userSecret)
        else:
            return cls(user_details.get("userId"), user_details.get("userSecret"))
