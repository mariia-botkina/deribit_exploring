from dataclasses import fields
from typing import Tuple, List, Dict, Any, Union

from scipy.stats import norm

from math import sqrt, log
from model import SymbolData, OptionData


def get_names_of_attributes(my_tuple: Tuple):
    return [item.name for item in my_tuple]


def get_list_of_symbols_data(list_of_dictionaries: List[Dict[str, Any]]) -> List[SymbolData]:
    list_of_symbols_data: List[SymbolData] = []

    for dictionary in list_of_dictionaries:
        symbol_data_dict: Dict[str, Any] = dict.fromkeys(get_names_of_attributes(fields(SymbolData)))
        for key in dictionary.keys():
            symbol_data_dict[key] = dictionary[key]

        list_of_symbols_data.append(SymbolData(*symbol_data_dict.values()))

    return list_of_symbols_data


def get_list_of_call_and_put_data(options_prices: List[Dict[str, Any]]) \
        -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    options_call: List[Dict[str, Union[int, float, bool, str]]] = []
    options_put: List[Dict[str, Union[int, float, bool, str]]] = []
    for option in options_prices:
        if option['instrument_name'][-1] == 'C':
            options_call.append(option)
        else:
            options_put.append(option)

    options_call.sort(key=lambda x: x['instrument_name'])
    options_put.sort(key=lambda x: x['instrument_name'])
    return options_call, options_put


def create_option_data(call: Dict[str, Any], put: Dict[str, Any], symbols_data: Dict[str, Dict[str, Any]]) \
        -> Union[None, OptionData]:
    option_data_dict: Dict[str, Any] = dict.fromkeys(get_names_of_attributes(fields(OptionData)))

    if call['ask_price'] is not None and put['ask_price'] is not None:
        option_data_dict['ask_price'] = min(call['ask_price'], put['ask_price']) * call['underlying_price']
        if option_data_dict['ask_price'] == call['ask_price']:
            option_data_dict['ask_type'] = 'call'
        else:
            option_data_dict['ask_type'] = 'put'
    elif call['ask_price'] is None and put['ask_price'] is None:
        return None
    else:
        if call['ask_price'] is None:
            option_data_dict['ask_price'] = put['ask_price'] * call['underlying_price']
            option_data_dict['ask_type'] = 'put'
        else:
            option_data_dict['ask_price'] = call['ask_price'] * call['underlying_price']
            option_data_dict['ask_type'] = 'call'

    if call['bid_price'] is not None and put['bid_price'] is not None:
        option_data_dict['bid_price'] = min(call['bid_price'], put['bid_price']) * call['underlying_price']
        if option_data_dict['bid_price'] == call['bid_price']:
            option_data_dict['bid_type'] = 'call'
        else:
            option_data_dict['bid_type'] = 'put'
    elif call['bid_price'] is None and put['bid_price'] is None:
        return None
    else:
        if call['bid_price'] is None:
            option_data_dict['bid_price'] = put['bid_price'] * call['underlying_price']
            option_data_dict['bid_type'] = 'put'
        else:
            option_data_dict['bid_price'] = call['bid_price'] * call['underlying_price']
            option_data_dict['bid_type'] = 'call'

    option_data_dict['name'] = call['instrument_name'][:-2]
    option_data_dict['strike'] = symbols_data[option_data_dict['name']]['strike']
    option_data_dict['maturity'] = (symbols_data[option_data_dict['name']]['expiration_timestamp'] -
                                    symbols_data[option_data_dict['name']]['creation_timestamp']) / 31536000000
    option_data_dict['underlying_price'] = call['underlying_price']

    return OptionData(*option_data_dict.values())


def calculate_ask_bid_volatility(option: OptionData):
    option.ask_volatility = calculate_volatility(option=option, price_type=option.ask_type, ask_price=option.ask_price)
    option.bid_volatility = calculate_volatility(option=option, price_type=option.bid_type, ask_price=option.bid_price)

    print(option.ask_volatility, option.bid_volatility)
    b = 2


def calculate_next_volatility(price_type: str, ask_price: float, T: float, X: float, S: float, sigma: float):
    d1 = (log(S / X) + sigma ** 2 / 2 * T) / (sigma * sqrt(T))
    d2 = d1 - sigma * sqrt(T)

    if price_type == 'call':
        N1 = norm.cdf(d1)
        N2 = norm.cdf(d2)
        f = ask_price - S * N1 + X * N2
    else:
        N1 = norm.cdf(-d1)
        N2 = norm.cdf(-d2)
        f = ask_price - X * N2 + S * N1
    f_derivative = S * norm.pdf(d1) * sqrt(T)

    new_sigma = sigma - f / f_derivative
    return new_sigma


def calculate_volatility(option: OptionData, price_type: str, ask_price: float):
    number_of_iterations = 100
    difference = 0.0001

    sigma1: float = 0.5
    for _ in range(number_of_iterations):
        sigma2 = calculate_next_volatility(price_type=price_type, ask_price=ask_price, T=option.maturity,
                                           X=option.strike, S=option.underlying_price, sigma=sigma1)
        if abs(sigma1 - sigma2) < difference:
            break
        else:
            sigma1 = sigma2

    return sigma2
