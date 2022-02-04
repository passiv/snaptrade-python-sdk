from snaptrade.models.base_model import BaseModel
from snaptrade.utils import SnapTradeUtils
from types import SimpleNamespace

class APIVersion(BaseModel):
    def __init__(self, version):
        self.version = version if version else "Unknown"

    _gen_str_params = ("version",)

class APIStatus(BaseModel):
    def __init__(self, version, timestamp, online):
        self.version = version
        self.timestamp = timestamp if timestamp else SnapTradeUtils.get_utc_time(string_format="%Y-%m-%d:T%H:%m:%S.%fZ")
        self.online = True if online else False

    _gen_str_params = ("version", "timestamp", "online")

    @classmethod
    def init_from_status_details(cls, api_status):
        if type(api_status) == SimpleNamespace:
            version = APIVersion(api_status.version)
            timestamp = api_status.timestamp
            online = api_status.online
        else:
            version = APIVersion(api_status.get("version"))
            timestamp = api_status.get("timestamp")
            online = api_status.get("online")

        return APIStatus(version, timestamp, online)