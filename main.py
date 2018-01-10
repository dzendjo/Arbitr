from arbitr import Arbitr
import time


a = Arbitr()

while True:
    bitfinex_prices = a.get_bitfinex_prices('tBTCUSD,tETHUSD')
    bittrex_prices = a.get_bittrex_prices('USDT-BTC,USDT-ETH')

    BTCUSD_list = [bitfinex_prices['tBTCUSD'], bittrex_prices['USDT-BTC']]
    ETHUSD_list = [bitfinex_prices['tETHUSD'], bittrex_prices['USDT-ETH']]

    print('='*60)
    print('BTC-USD {}, difference = {}'.format(BTCUSD_list, (max(BTCUSD_list) - min(BTCUSD_list)) * 100 / min(BTCUSD_list)))
    print('ETH-USD {}, difference = {}'.format(ETHUSD_list, (max(ETHUSD_list) - min(ETHUSD_list)) * 100 / min(ETHUSD_list)))

    time.sleep(10)
    # difference_BTCUSD = bitfinex_prices('tBTCUSD') -



