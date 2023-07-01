from dataclasses import fields
from typing import Tuple, List, Dict, Any

from model import SymbolData


def get_names_of_attributes(my_tuple: Tuple):
    return [item.name for item in my_tuple]


def get_list_of_symbols_data(list_of_dictionaries: List[Dict[str, Any]]) -> List[SymbolData]:
    list_of_symbols_data: List[SymbolData] = []

    for dictionary in list_of_dictionaries:
        symbol_data__dict: Dict[str, Any] = dict.fromkeys(get_names_of_attributes(fields(SymbolData)))
        for key in dictionary.keys():
            symbol_data__dict[key] = dictionary[key]

        list_of_symbols_data.append(SymbolData(*symbol_data__dict.values()))

    return list_of_symbols_data
