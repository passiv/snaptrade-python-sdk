from snaptrade.models.base_model import BaseModel
from snaptrade.utils import SnapTradeUtils


class APIVersion(BaseModel):
    def __init__(self, version):
        self.version = version if version else "Unknown"

    _gen_str_params = ("version",)


class APIStatus(BaseModel):
    def __init__(self, status):
        self.version = APIVersion(status.version)
        self.timestamp = (
            status.timestamp
            if status.timestamp
            else SnapTradeUtils.get_utc_time(string_format="%Y-%m-%d:T%H:%m:%S.%fZ")
        )
        self.online = True if status.online else False

    _gen_str_params = ("version", "timestamp", "online")


class ErrorMessage(BaseModel):
    def __init__(self, response, connection_error=False):
        if connection_error:
            self.status_code = 502
            self.detail = "Failed to connect to api server"
            self.code = 0000
        else:
            self.status_code = response.status_code
            self.detail = response.json().get("detail")
            self.code = response.json().get("code")

    _gen_str_params = ("status_code", "code", "detail")
