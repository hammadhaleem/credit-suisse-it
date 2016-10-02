import datetime
from threading import Thread
from time import sleep

from arbitrage import stock_trader_arbitrage
from exchange_layer import df_from_sql, to_int_symbol, df_to_sql
import pandas as pd

from moving_average import trader_moving_avg


def algo_trader(layer, tradeFrequency):
    symbol = '''select DISTINCT symbol from  stock_price_data limit 1000;'''
    symbols = list(df_from_sql(symbol).symbol.unique())

    exchanges = '''select DISTINCT exchange from  stock_price_data limit 1000;'''
    exchanges = list(df_from_sql(exchanges).exchange.unique())

    print("Exchanges  : {exchange}".format(exchange=",".join(exchanges)))
    print("Symbol  : {symbols}".format(symbols=",".join(symbols)))

    count = 1
    while True:
        threads = []
        for stock in symbols:
            stock_thread = Thread(target=stock_trader_arbitrage, args=(exchanges, stock, layer))
            stock_thread.start()
            threads.append(stock_thread)
            pass

        # join all the threads
        for th in threads:
            th.join()

        count += 1
        if count % 10 == 0:

            for stock in symbols:
                stock_thread = Thread(target=trader_moving_avg, args=(exchanges, stock, layer))
                stock_thread.start()
                # threads.append(stock_thread)

            # sleep(tradeFrequency)
