import datetime
from threading import Thread
from time import sleep
from exchange_layer import df_from_sql, to_int_symbol, df_to_sql
import pandas as pd


def stock_trader_arbitrage(exchanges, symbol, layer):
    team_information = layer.get_team_data()
    try:
        key = u'' + str(to_int_symbol(symbol))
        share_have = float(team_information[key])
    except Exception as e:
        share_have = 0

    sell_max_shares = 3000
    max_sell_price = -99999999
    global_exchange_sell = 1

    min_buy_price = 99999999999
    global_exchange_buy = 1
    trades = []
    for exchange in exchanges:
        try:
            price = layer.get_market_data(exchange_id=exchange, stock_symbol=symbol)
            current_bid = price['bid']
            current_ask = price['ask']
        except Exception as e:
            return None

        if current_bid > max_sell_price:  # and current_ask > mean_ask:
            max_sell_price = current_bid
            global_exchange_sell = exchange

        if current_ask < min_buy_price:  # and current_bid < mean_bid:
            min_buy_price = current_ask
            global_exchange_buy = exchange

    stri = ""
    if global_exchange_buy != global_exchange_sell and max_sell_price - min_buy_price > 0.1:
        qty = 100  # int(sell_max_shares/ current_bid)
        trades.append({
            'exchange_id': int(global_exchange_buy),
            'type': 'buy',
            'symbol': to_int_symbol(symbol),
            'qty': qty,
            'price': min_buy_price,
            'market': True
        })

        trades.append({
            'exchange_id': int(global_exchange_sell),
            'type': 'sell',
            'symbol': to_int_symbol(symbol),
            'qty': qty,
            'price': max_sell_price,
            'market': True
        })

        try:
            trade_list = []

            try:
                key = u''+str(to_int_symbol(symbol))
                # print(team_information, key)
                share_have = float(team_information[key])
            except Exception as e:
                share_have = 0

            for trade in trades:
                if trade['type'] == 'sell':
                    if share_have == 0 :
                        trade['qty'] = share_have+1
                    else:
                        trade['qty'] = share_have

                if trade['type'] == 'buy' and qty + share_have > sell_max_shares:
                    trade['qty'] = qty

                if True:
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
                    sleep(0.10)
                    try:
                        json = str(td['status'])
                    except:
                        try:
                            json = str(td['message'])
                        except:
                            print(td)
                            json = None
                            pass
                        pass

                    stri = "{0}   {1}".format(stri,
                                              '''[Trade] exchange {exchange_id} {type} stock : {symbol} quantity {qty} price {price} {json}'''.format(
                                                  exchange_id=trade['exchange_id'],
                                                  type=trade['type'],
                                                  symbol=trade['symbol'],
                                                  qty=trade['qty'],
                                                  price=trade['price'],
                                                  json=json
                                              ))

                    trade['json'] = str(td)
                    trade['time'] = datetime.datetime.now()

                    trade_list.append(trade)
            df_to_sql(pd.DataFrame(trade_list), 'ledger')
            print(stri)
            sleep(0.25)
        except Exception as e:
            print("Runtime ", e)
            pass

