import requests
import json


class Arbitr:

    def __init__(self):
        self.URL_BITFINEX = 'https://api.bitfinex.com/v2/tickers?symbols='

    def get_bitfinex_prices(self, pairs):
        res = requests.request('GET', self.URL_BITFINEX + pairs)
        print(res.read())
        response_list = json.loads(res.text)
        print(response_list)
