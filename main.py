from typing import List
import requests
import json

from utils import get_list_of_dataclasses


if __name__ == '__main__':
    res = requests.get(
        "https://test.deribit.com/api/v2/public/get_instruments?currency=BTC&settlement_period=perpetual")
    result: List = json.loads(res.text)['result']

    list_of_dataclasses = get_list_of_dataclasses(result)

    a = 1
