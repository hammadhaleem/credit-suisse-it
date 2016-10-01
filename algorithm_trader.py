from threading import Thread
from time import sleep
from exchange_layer import df_from_sql


def to_int_symbol(symbol):
    return str(symbol.split("_")[1])


def stock_trader(exchanges, symbol, layer):

    query = '''
            select *
            from
                stock_price_data where symbol = '{symbol_traded}'
            order by time
            desc limit 1000;
        '''.format(symbol_traded=symbol)

    df = df_from_sql(query)

    for exchange in exchanges:
        mask = ((df.exchange == exchange) & (df.symbol == symbol))
        df_for_exchange = df[mask]
        last_time = df_for_exchange.time.max()

        mean_bid = df_for_exchange.bid.mean()
        mean_ask = df_for_exchange.bid.mean()

        last_price_mask = (df.time == last_time)
        last_row = df_for_exchange[last_price_mask]

        current_bid = last_row.iloc[0]['bid']
        current_ask = last_row.iloc[0]['ask']
        qty = 10 ** 3
        if current_ask > mean_ask:
            trade = layer.buy_sell_market(
                exchange_id=to_int_symbol(exchange),
                type='sell',
                symbol=to_int_symbol(symbol),
                qty= qty
            )

            print('[Trade] Bought {symbol} at exchange {exchange} quantity {qty} Action Sell'.format(symbol=symbol,
                                                                                                     exchange=exchange,
                                                                                                     qty=qty))


        if current_bid < mean_bid:
            trade = layer.buy_sell_market(
                exchange_id=to_int_symbol(exchange),
                type='buy',
                symbol=to_int_symbol(symbol),
                qty= qty
            )

            print('[Trade] Bought {symbol} at exchange {exchange} quantity {qty} Action Sell'.format(symbol=symbol,
                                                                                                     exchange=exchange,
                                                                                                     qty=qty))


def algo_trader(layer, tradeFrequency):
    sleep(10)

    symbol = '''select DISTINCT symbol from  stock_price_data limit 1000;'''
    symbols = list(df_from_sql(symbol).symbol.unique())

    exchanges = '''select DISTINCT exchange from  stock_price_data limit 1000;'''
    exchanges = list(df_from_sql(exchanges).exchange.unique())

    print("Exchanges  : {exchange}".format(exchange=",".join(exchanges)))
    print("Symbol  : {symbols}".format(symbols = ",".join(exchanges)))

    if True:
        threads = []
        for stock in symbols :
            stock_thread = Thread(target=stock_trader, args=(exchanges, stock, layer))
            stock_thread.start()

        # join all the threads
        for th in threads:
            th.join()

        sleep(tradeFrequency)

