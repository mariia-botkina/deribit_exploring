from dataclasses import fields
from typing import Tuple, List, Dict, Any, Union

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


def get_list_of_call_and_put_data(options_prices: List[Dict[str, Union[int, float, bool, str]]]) \
        -> Tuple[List[Dict[str, Union[int, float, bool, str]]], List[Dict[str, Union[int, float, bool, str]]]]:
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


def create_option_data(call: Dict[str, Union[int, float, bool, str]], put: Dict[str, Union[int, float, bool, str]],
                       symbols_data: Dict[str, Dict[str, Union[int, float, None]]]) -> Union[None, OptionData]:
    option_data_dict: Dict[str, Any] = dict.fromkeys(get_names_of_attributes(fields(OptionData)))

    if call['ask_price'] is not None and put['ask_price'] is not None:
        option_data_dict['ask_price'] = min(call['ask_price'], put['ask_price'])
        if option_data_dict['ask_price'] is call['ask_price']:
            option_data_dict['ask_type'] = 'call'
        else:
            option_data_dict['ask_type'] = 'put'
    elif call['ask_price'] is None and put['ask_price'] is None:
        return None
    else:
        match call['ask_price']:
            case None:
                option_data_dict['ask_price'] = put['ask_price']
                option_data_dict['ask_type'] = 'put'
            case _:
                option_data_dict['ask_price'] = call['ask_price']
                option_data_dict['ask_type'] = 'call'

    if call['bid_price'] is not None and put['bid_price'] is not None:
        option_data_dict['bid_price'] = min(call['bid_price'], put['bid_price'])
        if option_data_dict['bid_price'] is call['bid_price']:
            option_data_dict['bid_type'] = 'call'
        else:
            option_data_dict['bid_type'] = 'put'
    elif call['bid_price'] is None and put['bid_price'] is None:
        return None
    else:
        match call['bid_price']:
            case None:
                option_data_dict['bid_price'] = put['bid_price']
                option_data_dict['bid_type'] = 'put'
            case _:
                option_data_dict['bid_price'] = call['bid_price']
                option_data_dict['bid_type'] = 'call'

    option_data_dict['name'] = call['instrument_name'][:-2]
    option_data_dict['strike'] = symbols_data[option_data_dict['name']]['strike']
    option_data_dict['maturity'] = (symbols_data[option_data_dict['name']]['expiration_timestamp'] - symbols_data[option_data_dict['name']]['creation_timestamp']) / 31536000000
    option_data_dict['underlying_price'] = call['underlying_price']

    return OptionData(*option_data_dict.values())
