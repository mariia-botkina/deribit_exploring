from typing import Dict, List
import requests
import json


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
                dictionary_keys = ' '.join(f.readlines())

            if f'{key}: {key_type}' not in dictionary_keys:
                with open('request_attributes.txt', 'a') as f:
                    f.writelines(f'{key}: {key_type}\n')


if __name__ == '__main__':
    res = requests.get(
        "https://test.deribit.com/api/v2/public/get_instruments?currency=BTC&settlement_period=perpetual")
    result: List = json.loads(res.text)['result']
    get_all_request_attributes(result)

    # fields = [f'{item.name}: Optional[{get_type(item.type)}]' for item in fields(SymbolData)]
    # print('\n'.join(fields))
    a = 0