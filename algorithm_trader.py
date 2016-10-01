import datetime
from threading import Thread
from time import sleep
from exchange_layer import df_from_sql, to_int_symbol, df_to_sql
import pandas as pd


def trader_moving_avg(exchanges, symbol, layer):
    query = '''
            select *
            from
                stock_price_data where symbol = '{symbol_traded}'
            order by time
            desc limit 1000;
        '''.format(symbol_traded=symbol)

    df = df_from_sql(query)
    df['exchange']= df.exchange.apply(lambda x: int(x))
    team_information = layer.get_team_data()

    mean_bid = df[df.exchange == 1].bid.mean()
    mean_ask = df[df.exchange == 1].ask.mean()

    final_bid = mean_bid
    final_ask = mean_ask

    bid_exchange = -1
    ask_exchange = -1

    price = layer.get_market_data(exchange_id=1, stock_symbol=symbol)
    if price is not None:
        for exchange in exchanges:
            mean_bid = df[df.exchange == int(exchange)].bid.mean()
            mean_ask = df[df.exchange == int(exchange)].ask.mean()

            price = layer.get_market_data(exchange_id=exchange, stock_symbol=symbol)
            # print(price,team_information[u'cash'])
            current_bid = price['bid']
            current_ask = price['ask']
            if mean_bid < current_bid:
                if current_bid > final_bid:
                    final_bid = current_bid
                    bid_exchange = exchange

            if mean_ask > current_ask:
                if current_ask < final_ask:
                    final_ask = current_ask
                    ask_exchange = exchange

        owned = team_information[u'' + str(to_int_symbol(symbol))]
        trades = []
        if bid_exchange != -1:
            trades.append({
                'exchange_id': int(bid_exchange),
                'type': 'buy',
                'symbol': to_int_symbol(symbol),
                'qty': int(owned) / 2,
                'market': True
            })

        # print((team_information[u'cash']), final_ask,team_information)
        owned = int(float(team_information[u'cash']) / final_ask)
        if ask_exchange != -1:
            trades.append({
                'exchange_id': int(ask_exchange),
                'type': 'sell',
                'symbol': to_int_symbol(symbol),
                'qty': owned,
                'market': True
            })

        if len(trades) > 0 :
            stri = ""
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

                    stri = stri + "   " + '''[Trade-Avg-moving] exchange {exchange_id} {type} stock : {symbol} quantity {qty} price {price}'''.format(
                        exchange_id=trade['exchange_id'],
                        type=trade['type'],
                        symbol=trade['symbol'],
                        qty=trade['qty'],
                        price=trade['price']
                    )

                    trade['json'] = str(td)
                    trade['time'] = datetime.datetime.now()
                    trade_list.append(trade)

                df_to_sql(pd.DataFrame(trade_list), 'ledger')
                print(" ", stri)
            except Exception as e:
                print("Runtime ", e)
                pass


def stock_trader_arbitrage(exchanges, symbol, layer):
    sell_max_shares = 1000
    max_sell_price = -99999999
    global_exchange_sell = 1

    min_buy_price = 99999999999
    global_exchange_buy = 1
    trades = []
    for exchange in exchanges:

        price = layer.get_market_data(exchange_id=exchange, stock_symbol=symbol)
        current_bid = price['bid']
        current_ask = price['ask']

        if current_bid > max_sell_price:  # and current_ask > mean_ask:
            max_sell_price = current_bid
            global_exchange_sell = exchange

        if current_ask < min_buy_price:  # and current_bid < mean_bid:
            min_buy_price = current_ask
            global_exchange_buy = exchange

    stri = ""
    if global_exchange_buy != global_exchange_sell and max_sell_price - min_buy_price > 0.1:
        qty = sell_max_shares  # int(sell_max_shares/ current_bid)
        trades.append({
            'exchange_id': int(global_exchange_buy),
            'type': 'buy',
            'symbol': to_int_symbol(symbol),
            'qty': qty,
            'price': min_buy_price,
            'market': False
        })

        trades.append({
            'exchange_id': int(global_exchange_sell),
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

                stri = stri + "   " + '''[Trade] exchange {exchange_id} {type} stock : {symbol} quantity {qty} price {price}'''.format(
                    exchange_id=trade['exchange_id'],
                    type=trade['type'],
                    symbol=trade['symbol'],
                    qty=trade['qty'],
                    price=trade['price']
                )

                trade['json'] = str(td)
                trade['time'] = datetime.datetime.now()

                trade_list.append(trade)
            df_to_sql(pd.DataFrame(trade_list), 'ledger')
            print(" ", stri)
        except Exception as e:
            print("Runtime ", e)
            pass


def algo_trader(layer, tradeFrequency):
    symbol = '''select DISTINCT symbol from  stock_price_data limit 1000;'''
    symbols = list(df_from_sql(symbol).symbol.unique())

    exchanges = '''select DISTINCT exchange from  stock_price_data limit 1000;'''
    exchanges = list(df_from_sql(exchanges).exchange.unique())

    print("Exchanges  : {exchange}".format(exchange=",".join(exchanges)))
    print("Symbol  : {symbols}".format(symbols=",".join(exchanges)))

    count = 0
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

        sleep(tradeFrequency)
        count += 1

        if count % 10 == 1:
            team_information = layer.get_team_data()
            print(team_information)

            for stock in symbols:
                stock_thread = Thread(target=trader_moving_avg, args=(exchanges, stock, layer))
                stock_thread.start()
                threads.append(stock_thread)
