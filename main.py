from arbitr import Arbitr
import time


a = Arbitr('pairs_data.csv')
# print(a.universal_pairs)
# print(a.get_all_pairs_by_market('Binance'))
# print(a.get_bitfinex_prices(a.get_all_pairs_by_market('Bitfinex')))
# print(a.get_bittrex_prices(a.get_all_pairs_by_market('bittrex')))
# print(a.get_binance_prices(a.get_all_pairs_by_market('binance')))
# print(a.get_kraken_pricesices(a.get_all_pairs_by_market('kraken')))
# print(a.get_all_pairs_prices())
# print(a.get_min_in_list([0.0001448, 0.00014499, None, 0.00014466]))
# print(a.get_max_in_list([0.0001448, 0.00014499, None, 0.00014466]))

while True:
    a.print_all_defferences()
    time.sleep(10)




