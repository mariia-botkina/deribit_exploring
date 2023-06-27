from typing import List, Dict, Union
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

    url_option = 'https://test.deribit.com/api/v2/public/get_book_summary_by_currency'
    params_option: Dict[str, str] = {
        'currency': 'BTC',
        'kind': 'option',

    }

    opt_cost_request: Response = requests.get(url=url_option, params=params_option)
    option_cost: List[Dict[str, Union[int, float, bool, str]]] = json.loads(opt_cost_request.text)['result']

    a = 1
