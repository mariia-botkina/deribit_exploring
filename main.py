from dataclasses import dataclass
import requests
import json


def make_dc(d, name='dataclass'):
    @dataclass
    class Wrapped:
        __annotations__ = {k: type(v) for k, v in d.items()}  # annotations are protected
        annotations = __annotations__

    Wrapped.__qualname__ = Wrapped.__name__ = name

    return Wrapped


if __name__ == '__main__':
    res = requests.get(
        "https://test.deribit.com/api/v2/public/get_instruments?currency=BTC&settlement_period=perpetual")
    result: list = json.loads(res.text)['result']

    data = [make_dc(item) for item in result]
    a = 1
