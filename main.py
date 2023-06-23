from dataclasses import dataclass, fields
from typing import List, Optional, Tuple
import requests
import json


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


def get_names_of_attributes(my_tuple: Tuple):
    return [item.name for item in my_tuple]


if __name__ == '__main__':
    res = requests.get(
        "https://test.deribit.com/api/v2/public/get_instruments?currency=BTC&settlement_period=perpetual")
    result: List = json.loads(res.text)['result']

    list_of_dataclasses = []
    for dictionary in result:
        my_dict = dict.fromkeys(get_names_of_attributes(fields(SymbolData)))
        for key in dictionary.keys():
            my_dict[key] = dictionary[key]
        list_of_dataclasses.append(SymbolData(*my_dict.values()))

    a = 1
