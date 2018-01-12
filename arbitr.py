import requests
import json
import csv
import sys

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

korbit
bitstamp
huobi
hitbtc
exmo
Koinex
"""

class Arbitr:
    # https: // api.kraken.com / 0 / public / Ticker?pair = XBTUSD

    def __init__(self, csv_file_name):
        self.csv_file_name = csv_file_name
        self.URL_BITFINEX = 'https://api.bitfinex.com/v2/tickers?symbols='
        self.URL_BITTREX = 'https://bittrex.com/api/v1.1/public/getticker?market='
        self.URL_KRAKEN = 'https://api.kraken.com/0/public/Ticker?pair='
        self.URL_BINANCE = 'https://api.binance.com/api/v1/ticker/price?symbol='
        self.names_of_market, self.universal_pairs = self.get_pair_list()

    def get_all_pairs_by_market(self, market_name):
        market_name_chaked = market_name.capitalize()
        all_pairs_list = []
        with open(self.csv_file_name) as csv_file:
            dict_reader = csv.DictReader(csv_file, delimiter=";")
            try:
                for item in dict_reader:
                    all_pairs_list.append(item[market_name_chaked])
            except Exception:
                return 'Ошибка в названии биржи: ' + str(sys.exc_info()[1])
        return all_pairs_list

    def get_bitfinex_prices(self, pairs):
        res = requests.request('GET', self.URL_BITFINEX + ','.join(pairs))
        response_list = json.loads(res.text)
        for i in range(len(pairs)):
            if pairs[i] == 'None':
                response_list.insert(i, 'None')
        pair_dict = {}
        for pair, key in zip(response_list, self.universal_pairs.keys()):
            try:
                pair_dict[key] = float(pair[-4])
            except Exception:
                pair_dict[key] = None
        return pair_dict

    def get_bittrex_prices(self, pairs):
        pair_dict = {}
        for pair, key in zip(pairs, self.universal_pairs.keys()):
            if pair == 'None':
                pair_dict[key] = 'None'
                continue
            res = requests.request('GET', self.URL_BITTREX + pair)
            response_dict = json.loads(res.text)
            pair_dict[key] = float(response_dict['result']['Last'])
        return pair_dict

    def get_binance_prices(self, pairs):
        pair_dict = {}
        for pair, key in zip(pairs, self.universal_pairs.keys()):
            if pair == 'None':
                pair_dict[key] = 'None'
                continue
            res = requests.request('GET', self.URL_BINANCE + pair)
            response_dict = json.loads(res.text)
            pair_dict[key] = float(response_dict['price'])
        return pair_dict

    def get_kraken_prices(self, pairs):
        pairs = pairs.split(',')
        pair_dict = {}
        for pair in pairs:
            res = requests.request('GET', self.URL_KRAKEN + pair)
            response_dict = json.loads(res.text)
            try:
                pair_dict[pair] = float(response_dict['result']['Last'])
            except Exception:
                pair_dict[pair] = None
        return pair_dict

    def get_pair_list(self):
         with open(self.csv_file_name, newline='') as csvfile:
            csvreader = csv.reader(csvfile)
            names_of_markets = csvreader.__next__()[0].split(';')
            universal_pairs = dict()
            for row in csvreader:
                row_list = row[0].split(';')
                universal_pairs[row_list[0]] = row_list[1:]
            return names_of_markets[1:], universal_pairs







