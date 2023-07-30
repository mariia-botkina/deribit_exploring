import json
from collections import defaultdict
from typing import List, Dict, Union

import matplotlib.pyplot as plt
import requests
from requests import Response
from sympy import nan

from model import SymbolData, OptionData
from utils import get_list_of_symbols_data, get_list_of_call_and_put_data, create_option_data, \
    calculate_ask_bid_volatility

if __name__ == '__main__':
    url = "https://deribit.com/api/v2/public/get_instruments"
    params: Dict[str, str] = {
        'currency': 'BTC',
        'kind': 'option',
    }

    res: Response = requests.get(url=url, params=params)
    result: List[Dict[str, Union[int, float, bool, str]]] = json.loads(res.text)['result']

    symbols_info: List[SymbolData] = get_list_of_symbols_data(result)
    
    symbols_data: Dict[str, Dict[str, Union[int, float, None]]] = defaultdict(defaultdict)
    for symbol in result:
        series = symbol['instrument_name'][:-2]
        symbols_data[series]['creation_timestamp'] = symbol['creation_timestamp']
        symbols_data[series]['expiration_timestamp'] = symbol['expiration_timestamp']
        symbols_data[series]['strike'] = symbol['strike']

    url_option = 'https://deribit.com/api/v2/public/get_book_summary_by_currency'
    params_option: Dict[str, str] = {
        'currency': 'BTC',
        'kind': 'option',
    }

    opt_prices_request: Response = requests.get(url=url_option, params=params_option)
    options_prices: List[Dict[str, Union[int, float, bool, str]]] = json.loads(opt_prices_request.text)['result']

    options_call, options_put = get_list_of_call_and_put_data(options_prices=options_prices)

    options_info: Dict[str, List[OptionData]] = defaultdict(list)
    for call, put in zip(options_call, options_put):
        series = call['instrument_name'].split('-')[0] + '-' + call['instrument_name'].split('-')[1]
        option = create_option_data(call=call, put=put, symbols_data=symbols_data)
        if option is not None:
            options_info[series].append(option)
    a = 2
    for series, option_items in options_info.items():
        ask_strikes: List[float] = []
        bid_strikes: List[float] = []
        ask_volatility, bid_volatility = [], []
        for item in option_items:
            item.ask_volatility, item.bid_volatility = calculate_ask_bid_volatility(item)
            if item.ask_volatility != nan:
                ask_strikes.append(item.strike)
                ask_volatility.append(item.ask_volatility)
            if item.bid_volatility != nan:
                bid_strikes.append(item.strike)
                bid_volatility.append(item.bid_volatility)
        plt.plot(ask_strikes, ask_volatility, 'bo', bid_strikes, bid_volatility, 'r+')
        plt.xlabel("Strike")
        plt.ylabel("Volatility")
        plt.title(f'{series}')
        plt.savefig(f'volatility_plots/{series}.png')
        plt.clf()

    b = 2