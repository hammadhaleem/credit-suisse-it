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
            order by time desc
            limit 500;
        '''.format(symbol_traded=symbol)

    df = df_from_sql(query)
    df['exchange'] = df.exchange.apply(lambda x: int(x))
    team_information = layer.get_team_data()

    mean_bid = df[df.exchange == 1].bid.mean()
    mean_ask = df[df.exchange == 1].ask.mean()

    avg_price  = (mean_ask + mean_bid)/ 2

    final_bid = avg_price
    final_ask = avg_price

    bid_exchange = -1
    ask_exchange = -1

    price = layer.get_market_data(exchange_id=1, stock_symbol=symbol)
    if price is not None:
        for exchange in exchanges:
            mean_bid = df[df.exchange == int(exchange)].bid.mean()
            mean_ask = df[df.exchange == int(exchange)].ask.mean()

            avg_price = (mean_ask + mean_bid) / 2

            price = layer.get_market_data(exchange_id=exchange, stock_symbol=symbol)
            # print(price,team_information[u'cash'])
            current_bid = price['bid']
            current_ask = price['ask']
            if avg_price < current_bid:
                if current_bid > final_bid:
                    final_bid = current_bid
                    bid_exchange = exchange

            if avg_price > current_ask:
                if current_ask < final_ask:
                    final_ask = current_ask
                    ask_exchange = exchange

        owned = float(team_information[u'' + str(to_int_symbol(symbol))])
        trades = []
        if bid_exchange != -1:
            trades.append({
                'exchange_id': int(bid_exchange),
                'type': 'sell',
                'symbol': to_int_symbol(symbol),
                'qty': int(owned) / 2,
                'market': False,
                'price' : final_bid
            })

        # print((team_information[u'cash']), final_ask,team_information)
        owned = int(float(team_information[u'cash']) / final_ask)
        if ask_exchange != -1:
            trades.append({
                'exchange_id': int(ask_exchange),
                'type': 'buy',
                'symbol': to_int_symbol(symbol),
                'qty': owned,
                'market': False,
                'price': final_ask
            })

        if len(trades) > 0:
            stri = ""
            try:
                trade_list = []
                share_have = float(team_information[str(to_int_symbol(symbol))])
                for trade in trades:
                    if trade['type'] == 'sell':
                        trade['qty'] = share_have+1
                    if trade['type'] == 'buy' and trade['qty'] + share_have < 2000:
                        trade['qty'] += 1

                    if trade['market'] is False:
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

                    try:
                        json = str(td['status'])
                    except:
                        json = None

                    stri = stri + "   " + '''[Trade-Avg-moving] exchange {exchange_id} {type} stock : {symbol} quantity {qty} price {price}'''.format(
                        exchange_id=trade['exchange_id'],
                        type=trade['type'],
                        symbol=trade['symbol'],
                        qty=trade['qty'],
                        price=trade['price'],
                        json=json
                    )

                    trade['json'] = str(td)
                    trade['time'] = datetime.datetime.now()
                    trade_list.append(trade)
                    sleep(0.5)

                df_to_sql(pd.DataFrame(trade_list), 'ledger')
                print(" ", stri)
            except Exception as e:
                print("Runtime ", e)
                pass
