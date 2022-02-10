from snaptrade.models.base_model import BaseModel


class Account(BaseModel):
    def __init__(
        self,
        account_id,
        account_name,
        account_number,
        account_type,
        brokerage_authorization_id,
        institution_name,
    ):
        self.account_id = account_id
        self.account_name = account_name
        self.account_number = account_number
        self.account_type = account_type
        self.brokerage_authorization_id = brokerage_authorization_id
        self.institution_name = institution_name

    _gen_str_params = ("institution_name", "account_name", "account_number")

    @classmethod
    def init_from_raw_data(cls, raw_accounts_data):
        initialized_accounts = []

        for account_data in raw_accounts_data:
            initialized_account = cls(
                account_id=account_data.id,
                account_name=account_data.name,
                account_number=account_data.number,
                account_type=account_data.meta.type,
                brokerage_authorization_id=account_data.brokerage_authorization,
                institution_name=account_data.meta.institution_name,
            )

            initialized_accounts.append(initialized_account)

        return initialized_accounts
