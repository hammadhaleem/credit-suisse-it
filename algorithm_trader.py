import datetime
from threading import Thread
from time import sleep, time
from exchange_layer import df_from_sql, sell_max_shares, to_int_symbol, df_to_sql
import pandas as pd


def trader_machine_learning(exchanges, symbol, layer):
    query = '''
            select *
            from
                stock_price_data where symbol = '{symbol_traded}'
            order by time
            desc limit 1000;
        '''.format(symbol_traded=symbol)


    df = df_from_sql(query)




def stock_trader_arbitrage(exchanges, symbol, layer):
    max_sell_price = -99999999
    global_exchange_sell = 1

    min_buy_price = 99999999999
    global_exchange_buy = 1
    trades = []
    for exchange in exchanges:

        price = layer.get_market_data(exchange_id=exchange,stock_symbol=symbol)
        current_bid = price['bid']
        current_ask = price['ask']

        if current_ask > max_sell_price: # and current_ask > mean_ask:
            max_sell_price = current_ask
            global_exchange_sell = exchange

        if current_bid < min_buy_price: # and current_bid < mean_bid:
            min_buy_price = current_bid
            global_exchange_buy = exchange

    if global_exchange_buy != global_exchange_sell and max_sell_price - min_buy_price > 0.1:
            qty = sell_max_shares #int(sell_max_shares/ current_bid)
            trades.append({
                'exchange_id': int(global_exchange_buy),
                'type':'buy',
                'symbol':to_int_symbol(symbol),
                'qty': qty,
                'price': min_buy_price,
                'market': False
            })

            trades.append({
                'exchange_id': int(global_exchange_buy),
                'type': 'sell',
                'symbol': to_int_symbol(symbol),
                'qty': qty,
                'price': max_sell_price,
                'market': False
            })

            try:
                trade_list = []
                for trade in trades:
                    if not trade['market']:
                        td = layer.buy_sell_limit(
                            exchange_id=trade['exchange_id'],
                            type=trade['type'],
                            symbol=trade['symbol'],
                            qty=trade['qty'],
                            price=trade['price']
                        )

                    else:
                        td = layer.buy_sell_market(
                            exchange_id=trade['exchange_id'],
                            type=trade['type'],
                            symbol=trade['symbol'],
                            qty=trade['qty']
                        )

                    stri = stri + "\n" + '''[Trade] exchange {exchange_id} {type} stock : {symbol} quantity {qty} price {price}'''.format(
                        exchange_id=trade['exchange_id'],
                        type=trade['type'],
                        symbol=trade['symbol'],
                        qty=trade['qty'],
                        price=trade['price']
                    )

                    trade['json'] = str(td)
                    trade['time'] = datetime.datetime.now()


                    trade_list.append(trade)
                df_to_sql(pd.DataFrame(trade_list),'ledger')
                print(stri)
            except Exception as e:
                print("Runtime ",e)
                pass


def algo_trader(layer, tradeFrequency):
    sleep(10)

    symbol = '''select DISTINCT symbol from  stock_price_data limit 1000;'''
    symbols = list(df_from_sql(symbol).symbol.unique())

    exchanges = '''select DISTINCT exchange from  stock_price_data limit 1000;'''
    exchanges = list(df_from_sql(exchanges).exchange.unique())

    print("Exchanges  : {exchange}".format(exchange=",".join(exchanges)))
    print("Symbol  : {symbols}".format(symbols = ",".join(exchanges)))

    while True:
        threads = []
        for stock in symbols :
            stock_thread = Thread(target=stock_trader_arbitrage, args=(exchanges, stock, layer))
            stock_thread.start()

        # join all the threads
        for th in threads:
            th.join()

        sleep(tradeFrequency)

