from snaptrade.models.base_model import BaseModel


class Brokerage(BaseModel):
    def __init__(self, id, name, url):
        self.id = id
        self.name = name
        self.url = url

    _gen_str_params = ("name",)

    @classmethod
    def init_from_raw_data(cls, raw_brokerages_data):
        initialized_brokerages = [
            cls.init_brokerage_obj(brokerage_data)
            for brokerage_data in raw_brokerages_data
        ]
        return initialized_brokerages

    @classmethod
    def init_brokerage_obj(cls, brokerage_data):
        return cls(
            id=brokerage_data.id, name=brokerage_data.name, url=brokerage_data.url
        )


class Currency(BaseModel):
    def __init__(self, id, name, code):
        self.id = id
        self.name = name
        self.code = code

    _gen_str_params = (
        "code",
        "name",
    )

    @classmethod
    def init_from_raw_data(cls, raw_currencies_data):
        initialized_currencies = [
            cls.init_currency_obj(currency_data)
            for currency_data in raw_currencies_data
        ]
        return initialized_currencies

    @classmethod
    def init_currency_obj(cls, currency_data):
        return cls(currency_data.id, currency_data.name, currency_data.code)


class ExchangeRate(BaseModel):
    def __init__(self, src, dst, exchange_rate):
        self.src = src
        self.dst = dst
        self.exchange_rate = exchange_rate

    _gen_str_params = (
        "src",
        "dst",
        "exchange_rate",
    )

    @classmethod
    def init_from_raw_data(cls, raw_exchange_rates_data):
        if type(raw_exchange_rates_data) != list:
            return cls.init_exchange_rate_obj(raw_exchange_rates_data)
        else:
            initialized_exchange_rates = [
                cls.init_exchange_rate_obj(exchange_rate_data)
                for exchange_rate_data in raw_exchange_rates_data
            ]
            return initialized_exchange_rates

    @classmethod
    def init_exchange_rate_obj(cls, exchange_rate_data):
        return cls(
            src=Currency.init_currency_obj(exchange_rate_data.src),
            dst=Currency.init_currency_obj(exchange_rate_data.dst),
            exchange_rate=exchange_rate_data.exchange_rate,
        )


class SecurityType(BaseModel):
    def __init__(self, security_type_id, code, is_supported):
        self.id = security_type_id
        self.code = code
        self.is_supported = is_supported

    @classmethod
    def init_security_type_obj(cls, security_type_data):
        return cls(
            security_type_id=security_type_data.id,
            code=security_type_data.code,
            is_supported=security_type_data.is_supported,
        )


class Exchange(BaseModel):
    def __init__(
        self, exchange_id, code, name, timezone, start_time, close_time, suffix
    ):
        self.id = exchange_id
        self.code = code
        self.name = name
        self.timezone = timezone
        self.start_time = start_time
        self.close_time = close_time
        self.suffix = suffix

    @classmethod
    def init_exchange_obj(cls, exchange_data):
        return cls(
            exchange_id=exchange_data.id,
            code=exchange_data.code,
            name=exchange_data.name,
            timezone=exchange_data.timezone,
            start_time=exchange_data.start_time,
            close_time=exchange_data.close_time,
            suffix=exchange_data.suffix,
        )


class UniversalSymbol(BaseModel):
    def __init__(
        self, symbol_id, ticker, description, currency, exchange, security_type
    ):
        self.id = symbol_id
        self.ticker = ticker
        self.description = description
        self.currency = currency
        self.exchange = exchange
        self.security_type = security_type

    _gen_str_params = (
        "ticker",
        "description",
    )

    @classmethod
    def init_from_raw_data(cls, raw_symbols_data):
        if type(raw_symbols_data) != list:
            return cls.init_universal_symbol_obj(raw_symbols_data)
        else:
            initialized_exchange_rates = [
                cls.init_universal_symbol_obj(symbol_data)
                for symbol_data in raw_symbols_data
            ]
            return initialized_exchange_rates

    @classmethod
    def init_universal_symbol_obj(cls, symbol_data):
        return cls(
            symbol_id=symbol_data.id,
            ticker=symbol_data.symbol,
            description=symbol_data.description,
            currency=Currency.init_currency_obj(symbol_data.currency),
            exchange=Exchange.init_exchange_obj(symbol_data.exchange),
            security_type=SecurityType.init_security_type_obj(symbol_data.type),
        )
