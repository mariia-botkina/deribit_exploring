from collections import defaultdict
from dataclasses import dataclass
from typing import List, Dict, Union, Optional
import requests
import json

from requests import Response

from model import SymbolData
from utils import get_list_of_symbols_data

if __name__ == '__main__':
    url = "https://deribit.com/api/v2/public/get_instruments"
    params: Dict[str, str] = {
        'currency': 'BTC',
        'kind': 'option',
    }

    res: Response = requests.get(url=url, params=params)
    result: List[Dict[str, Union[int, float, bool, str]]] = json.loads(res.text)['result']

    symbols_info: List[SymbolData] = get_list_of_symbols_data(result)

    url_option = 'https://deribit.com/api/v2/public/get_book_summary_by_currency'
    params_option: Dict[str, str] = {
        'currency': 'BTC',
        'kind': 'option',

    }

    opt_prices_request: Response = requests.get(url=url_option, params=params_option)
    options_prices: List[Dict[str, Union[int, float, bool, str]]] = json.loads(opt_prices_request.text)['result']

    ts_data: Dict[str, List[int]] = defaultdict(list)

    for data in options_prices:
        series = data['instrument_name'].split('-')[0] + data['instrument_name'].split('-')[1]
        ts_data[series].append(data['creation_timestamp'])

    """
        BTC-29JUN23-30000-P
        30000 - strike
        P - put
    """


    @dataclass
    class OptionData:
        maturity: float  # expiry - creation_timestamp -> years
        underlying_price: float  # from prices
        ask_price: Optional[float]  # min from put, call
        ask_type: str  # put or call
        bid_price: Optional[float]  # max from put, call
        bid_tyoe: str  # put or call
        strike: int  # from symbols info
        name: str  # BTC-29JUN23-30000


    ot_data: Dict[str, List[int]] = defaultdict(list)

    for data in result:
        series = data['instrument_name'].split('-')[0] + data['instrument_name'].split('-')[1]
        ot_data[series].append(data['option_type'])

    for series, ts_list in ts_data.items():
        print(series, max(ts_list) - min(ts_list), ot_data[series])

    a = 1
