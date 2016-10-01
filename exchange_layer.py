import json
import urllib2

## u'sYFDHpA1uLkKq6z3QwnCyg


class Exchange_layer():
    '''
    1. Buy on market
    2. Sell on market
    3. Buy on limit
    4. Sell on limit
    5. Read market data
    '''

    exchange_url = {
        1: 'http://cis2016-exchange1.herokuapp.com/api/orders/',
        2: 'http://cis2016-exchange2.herokuapp.com/api/orders/',
        3: 'http://cis2016-exchange3.herokuapp.com/api/orders/'
    }

    team_id = 'sYFDHpA1uLkKq6z3QwnCyg'

    def send_generic_post_requests(self, url, data):
        try:
            jsondata = json.dumps(data)
            postreq = urllib2.Request(url, jsondata)
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

    def test_buy_sell_market(self, exchange_id, type, symbol, qty):

        buy_url = "{exchange_url}".format(exchange_url=self.exchange_url[exchange_id])
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
        buy_url = "{exchange_url}".format(exchange_url=self.exchange_url[exchange_id])
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
        order_url = "{exchange_url}{uid}?next_stage".format(exchange_url=self.exchange_url[exchange_id],uid=uid)

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


