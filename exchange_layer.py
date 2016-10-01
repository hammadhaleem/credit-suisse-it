import json
import urllib2

import pandas as pd
from sqlalchemy import create_engine
from time import sleep

db_conn_url = "postgres://credit01:credit01@credit01.cnxiijjshvio.ap-southeast-1.rds.amazonaws.com:5432/credit01"

sql_engine = {}


class Exchange_layer():
    '''
    1. Buy on market
    2. Sell on market
    3. Buy on limit
    4. Sell on limit
    5. Read market data
    '''

    exchange_url = {
        1: 'http://cis2016-exchange1.herokuapp.com/api/',
        2: 'http://cis2016-exchange2.herokuapp.com/api/',
        3: 'http://cis2016-exchange3.herokuapp.com/api/'
    }

    team_id = 'sYFDHpA1uLkKq6z3QwnCyg'

    def send_generic_post_requests(self, url, data = None):
        try:
            if data != None:
                jsondata = json.dumps(data)
                postreq = urllib2.Request(url, jsondata)
                postreq.add_header('Content-Type', 'application/json')
                resp = urllib2.urlopen(postreq).read()
            else:
                postreq = urllib2.Request(url)
                postreq.add_header('Content-Type', 'application/json')
                resp = urllib2.urlopen(postreq).read()
            resp = json.loads(resp)
        except Exception as e:
            print(e)
            return None
        return resp


    def send_setup_request(self):
        register_post_fields = {
            "name": "codeNinja",
            "members": ['Hammad Haleem', 'Vikram Sambamurty', 'Irtaza Khan']
        }

        url = "http://cis2016-teamtracker.herokuapp.com/api/teams/"

        resp = self.send_generic_post_requests(url, register_post_fields)
        resp = json.loads(resp)
        team_id = resp['uid']
        self.team_id = team_id
        print(resp)
        return resp

    def get_market_data(self, exchange_id, stock_symbol = None):
        data_url = "{exchange_url}/market_data".format(exchange_url=self.exchange_url[exchange_id])
        resp = self.send_generic_post_requests(data_url)
        resp_list= []
        for elem in resp:
            elem['exchange'] = exchange_id
            resp_list.append(elem)
        resp = resp_list
        if stock_symbol is None:
            return resp

        for elem in resp:
            if elem['symbol'] == stock_symbol:
                return elem
        return None

    def test_buy_sell_market(self, exchange_id, type, symbol, qty):

        buy_url = "{exchange_url}orders/".format(exchange_url=self.exchange_url[exchange_id])
        data_buy_information = {
            "symbol": symbol,
            'side': type,
            'qty': qty,
            "team_uid": self.team_id,
            'order_type': 'market'
        }

        resp = self.send_generic_post_requests(buy_url, data_buy_information)
        print(resp)
        return resp

    def test_buy_sell_limit(self, exchange_id, type, symbol, qty, price):
        buy_url = "{exchange_url}orders/".format(exchange_url=self.exchange_url[exchange_id])
        data_buy_information = {
            "symbol": symbol,
            'side': type,
            'qty': qty,
            "team_uid": self.team_id ,
            'order_type': 'limit',
            'price': price
        }

        resp = self.send_generic_post_requests(buy_url, data_buy_information)
        return resp

    def cancel_order(self, uid, exchange_id):
        order_url = "{exchange_url}orders/{uid}?next_stage".format(exchange_url=self.exchange_url[exchange_id],uid=uid)

        data_buy_information = {
            "team_uid": self.team_id ,
            'id': uid
        }

        jsondata = json.dumps(data_buy_information)
        postreq = urllib2.Request(order_url, jsondata)
        postreq.get_method = lambda: 'DELETE'

        val = urllib2.urlopen(postreq).read()
        print(val)
        return val


def new_sql_engine(db):
    global sql_engine
    if db not in sql_engine:
        sql_engine[db] = create_engine(db_conn_url)
    return sql_engine[db]


def df_to_sql(df, table='stock_price_data', db='credit01'):
    engine = new_sql_engine(db)
    df.to_sql(table, engine, if_exists='append', index=False)
    print('Data saved in the table:{}'.format(table))
    return df


def df_from_sql(query, db='credit01'):  # xx
    print(query)
    engine = new_sql_engine(db)
    try:
        df = pd.read_sql_query(query, con=engine)
        print(df.head())
        return df
    except Exception as e:
        print(e)
        return None


def get_market_data_running(layer):
    while True:
        lis = []
        print("get_exchange_data")
        lis.extend(layer.get_market_data(exchange_id=1))
        lis.extend(layer.get_market_data(exchange_id=2))
        lis.extend(layer.get_market_data(exchange_id=3))
        df = pd.DataFrame(lis)
        df_to_sql(df)
        print(df.head())