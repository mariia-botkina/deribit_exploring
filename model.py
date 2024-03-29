from dataclasses import dataclass
from typing import Optional


@dataclass
class SymbolData:
    tick_size_steps: Optional[list]
    tick_size: Optional[float]
    taker_commission: Optional[int]
    strike: Optional[float]
    settlement_period: Optional[str]
    settlement_currency: Optional[str]
    rfq: Optional[bool]
    quote_currency: Optional[str]
    price_index: Optional[str]
    option_type: Optional[str]
    min_trade_amount: Optional[float]
    maker_commission: Optional[int]
    kind: Optional[str]
    is_active: Optional[bool]
    instrument_type: Optional[str]
    instrument_name: Optional[str]
    instrument_id: Optional[int]
    expiration_timestamp: Optional[int]
    creation_timestamp: Optional[int]
    counter_currency: Optional[str]
    contract_size: Optional[float]
    block_trade_tick_size: Optional[float]
    block_trade_min_trade_amount: Optional[int]
    block_trade_commission: Optional[float]
    base_currency: Optional[str]
    max_liquidation_commission: Optional[float]
    max_leverage: Optional[int]
    future_type: Optional[str]


@dataclass
class OptionData:
    maturity: float  # expiry - creation_timestamp -> years
    underlying_price: float  # from prices
    ask_price: Optional[float]  # min from put, call
    ask_type: str  # put or call
    bid_price: Optional[float]  # max from put, call
    bid_type: str  # put or call
    strike: float  # from symbols info
    name: str  # BTC-29JUN23-30000
    ask_volatility: Optional[float]
    bid_volatility: Optional[float]
