from dataclasses import fields
from typing import Tuple, List

from model import SymbolData


def get_names_of_attributes(my_tuple: Tuple):
    return [item.name for item in my_tuple]


def get_list_of_dataclasses(list_of_dictionaries: List):
    list_of_dataclasses = []
    for dictionary in list_of_dictionaries:
        my_dict = dict.fromkeys(get_names_of_attributes(fields(SymbolData)))
        for key in dictionary.keys():
            my_dict[key] = dictionary[key]
        list_of_dataclasses.append(SymbolData(*my_dict.values()))
    return list_of_dataclasses
