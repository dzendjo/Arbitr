import requests
import json

"""
1: USD-BTC
2: USD-ETH
3: ETH-BTC
4: XRP-BTC
5: BCH-BTC
6: LTC-BTC
8: IOTA-BTC
9: EOS-BTC
10: NEO-BTC
11: ETC-BTC
12: OMG-BTC
13: XMR-BTC
14: ZEC-BTC
15: DASH-BTC
16: SNT-BTC
17: QTUM-BTC
18: BTG-BTC
19: ETP-BTC
20: QASH-BTC
21: DATA-BTC
22: GNT-BTC
23: YYW-BTC
24: EDO-BTC
25: SAN-BTC
26: FUN-BTC
27: ZRX-BTC
28: AVT-BTC
29: SPK-BTC
30: BAT-BTC
31: MNA-BTC
32: MNA-BTC
33: TNB-BTC
34: RRT-BTC
"""

class Arbitr:
    # https: // api.kraken.com / 0 / public / Ticker?pair = XBTUSD

    def __init__(self):
        self.URL_BITFINEX = 'https://api.bitfinex.com/v2/tickers?symbols='
        self.URL_BITTREX = 'https://bittrex.com/api/v1.1/public/getticker?market='
        self.URL_KRAKEN = 'https://bittrex.com/api/v1.1/public/getticker?market='


    def get_bitfinex_prices(self, pairs):
        res = requests.request('GET', self.URL_BITFINEX + pairs)
        response_list = json.loads(res.text)
        pair_dict = {}
        for pair in response_list:
            pair_dict[pair[0]] = float(pair[-4])
        return pair_dict


    def get_bittrex_prices(self, pairs):
        pairs = pairs.split(',')
        pair_dict = {}
        for pair in pairs:
            res = requests.request('GET', self.URL_BITTREX + pair)
            response_dict = json.loads(res.text)
            pair_dict[pair] = float(response_dict['result']['Last'])
        return pair_dict

    def get_kraken_prices(self, pairs):
        pairs = pairs.split(',')
        pair_dict = {}
        for pair in pairs:
            res = requests.request('GET', self.URL_BITTREX + pair)
            response_dict = json.loads(res.text)
            pair_dict[pair] = float(response_dict['result']['Last'])
        return pair_dict









