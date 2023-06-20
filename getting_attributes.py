from typing import Dict
from dataclasses import dataclass
import requests
import json


@dataclass
class Data:
    tick_size_steps: list
    tick_size: float
    taker_commission: float
    strike: float
    settlement_period: str
    settlement_currency: str
    rfq: bool
    quote_currency: str
    price_index: str
    option_type: str
    min_trade_amount: float
    maker_commission: float
    kind: str
    is_active: bool
    instrument_type: str
    instrument_name: str
    instrument_id: int
    expiration_timestamp: int
    creation_timestamp: int
    counter_currency: str
    contract_size: float
    block_trade_tick_size: float
    block_trade_min_trade_amount: float
    block_trade_commission: float
    base_currency: str
    max_liquidation_commission: float
    max_leverage: int
    future_type: str
    block_trade_min_trade_amount: int
    taker_commission: int
    maker_commission: int


def get_type(attribute_type: type):
    attribute_type: str = str(attribute_type).replace("<class '", '')
    attribute_type: str = attribute_type.replace("'>", '')
    return attribute_type


def get_all_request_attributes(dictionary: list[Dict]):
    # clear the 'request_attributes.txt' file
    open('request_attributes.txt', 'w').close()
    for Dictionary in dictionary:
        for key in Dictionary.keys():
            key_type = get_type(type(Dictionary[key]))
            with open('request_attributes.txt', 'r+') as f:
                data = ' '.join(f.readlines())

            if f'{key}: {key_type}' not in data:
                with open('request_attributes.txt', 'a') as f:
                    f.writelines(f'{key}: {key_type}\n')


if __name__ == '__main__':
    res = requests.get(
        "https://test.deribit.com/api/v2/public/get_instruments?currency=BTC&settlement_period=perpetual")
    result: list = json.loads(res.text)['result']
    get_all_request_attributes(result)
