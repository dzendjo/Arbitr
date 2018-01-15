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

    def __init__(self, csv_file_name):
        self.csv_file_name = csv_file_name
        self.URL_BITFINEX = 'https://api.bitfinex.com/v2/tickers?symbols='
        self.URL_BITTREX = 'https://bittrex.com/api/v1.1/public/getticker?market='
        self.URL_KRAKEN = 'https://api.kraken.com/0/public/Ticker?pair='
        self.URL_BINANCE = 'https://api.binance.com/api/v1/ticker/price?symbol='
        self.URL_EXMO = 'https://api.exmo.com/v1/ticker/?pair='
        self.URL_HITBTC = 'https://api.hitbtc.com/api/2/public/ticker/'
        self.URL_POLONIEX = 'https://poloniex.com/public?command=returnTicker'
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

    def get_pair_list(self):
         with open(self.csv_file_name, newline='') as csvfile:
            csvreader = csv.reader(csvfile)
            names_of_markets = csvreader.__next__()[0].split(';')
            universal_pairs = dict()
            for row in csvreader:
                row_list = row[0].split(';')
                universal_pairs[row_list[0]] = row_list[1:]
            return names_of_markets[1:], universal_pairs

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
        pair_dict = {}
        for pair, key in zip(pairs, self.universal_pairs.keys()):
            if pair == 'None':
                pair_dict[key] = None
                continue
            res = requests.request('GET', self.URL_KRAKEN + pair)
            response_dict = json.loads(res.text)
            try:
                kraken_prefix = 'X' + pair[:3] + 'X' + pair[3:]
                pair_dict[key] = float(response_dict['result'][kraken_prefix]['c'][0])
            except Exception:
                pair_dict[key] = None
        return pair_dict

    def get_exmo_prices(self, pairs):
        pair_dict = {}
        for pair, key in zip(pairs, self.universal_pairs.keys()):
            if pair == 'None':
                pair_dict[key] = None
                continue
            res = requests.request('GET', self.URL_EXMO + pair)
            response_dict = json.loads(res.text)
            pair_dict[key] = float(response_dict[pair]['last_trade'])
        return pair_dict

    def get_hitbtc_prices(self, pairs):
        pair_dict = {}
        for pair, key in zip(pairs, self.universal_pairs.keys()):
            if pair == 'None':
                pair_dict[key] = None
                continue
            res = requests.request('GET', self.URL_HITBTC + pair)
            response_dict = json.loads(res.text)
            pair_dict[key] = float(response_dict['last'])
        return pair_dict

    def get_poloniex_prices(self, pairs):
        pair_dict = {}
        res = requests.request('GET', self.URL_POLONIEX)
        response_dict = json.loads(res.text)
        for pair, key in zip(pairs, self.universal_pairs.keys()):
            if pair == 'None':
                pair_dict[key] = None
                continue
            pair_dict[key] = float(response_dict[pair]['last'])
        return pair_dict

    def get_all_pairs_prices(self):
        pairs_prices_dict = {}
        bitfinex_prices = self.get_bitfinex_prices(self.get_all_pairs_by_market('Bitfinex'))
        bittrex_prices = self.get_bittrex_prices(self.get_all_pairs_by_market('Bittrex'))
        binance_prices = self.get_binance_prices(self.get_all_pairs_by_market('Binance'))
        kraken_prices = self.get_kraken_prices(self.get_all_pairs_by_market('Kraken'))
        exmo_prices = self.get_exmo_prices(self.get_all_pairs_by_market('Exmo'))
        hitbtc_prices = self.get_hitbtc_prices(self.get_all_pairs_by_market('Hitbtc'))
        poloniex_prices = self.get_poloniex_prices(self.get_all_pairs_by_market('Poloniex'))
        for pair in self.universal_pairs.keys():
            pairs_prices_dict[pair] = [
                bitfinex_prices[pair],
                bittrex_prices[pair],
                kraken_prices[pair],
                binance_prices[pair],
                exmo_prices[pair],
                hitbtc_prices[pair],
                poloniex_prices[pair]
            ]
        return pairs_prices_dict

    def get_min_in_list(self, price_list):
        min = 10000000
        index = 0
        for i in range(len(price_list)):
            try:
                price_list[i] = float(price_list[i])
            except Exception:
                continue
            if price_list[i] < min:
                min = price_list[i]
                index = i
        name_of_min_market = self.names_of_market[index]
        return (min, name_of_min_market)

    def get_max_in_list(self, price_list):
        max = 0
        index = 0
        for i in range(len(price_list)):
            try:
                price_list[i] = float(price_list[i])
            except Exception:
                continue
            if price_list[i] > max:
                max = price_list[i]
                index = i
        name_of_min_market = self.names_of_market[index]
        return (max, name_of_min_market)

    def print_all_defferences(self):
        pairs_prices_dict = self.get_all_pairs_prices()
        res_s = ''
        for pair in pairs_prices_dict:
            res_s += str(pair) + ': ' + str(pairs_prices_dict[pair]) + '    '
            min_list = self.get_min_in_list(pairs_prices_dict[pair])
            max_list = self.get_max_in_list(pairs_prices_dict[pair])
            difference = round((max_list[0] - min_list[0]) * 100 / min_list[0], 2)
            res_s += str(difference) + '%  ' + min_list[1] + ' --> ' + max_list[1] + '\n'
        print(res_s)







