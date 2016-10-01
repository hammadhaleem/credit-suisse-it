import json
import urllib2


stage = 2

def send_generic_post_requests(url , data):
    jsondata = json.dumps(data)
    postreq = urllib2.Request(url, jsondata)
    postreq.add_header('Content-Type', 'application/json')

    resp = urllib2.urlopen(postreq).read()
    return resp

def send_setup_request():
    register_post_fields = {
        "name": "Code-Ninja",
        "members": ['Hammad Haleem', 'Vikram Sambamurty', 'Irtaza Khan']
    }

    url = "http://cis2016-teamtracker.herokuapp.com/api/teams/"

    resp = send_generic_post_requests(url, register_post_fields)
    resp = json.loads(resp)
    print(resp)
    return resp


def test_buy_sell():
    buy_url = "http://cis2016-exchange1.herokuapp.com/api/orders/?next_stage"
    data_buy_information = {
        "symbol": "0005",
        'side': "buy",
        'qty' : 1,
        "team_uid":"WQKW1pUQiKdCw7TIzBnWwg",
        'order_type' : 'limit',
        'price' : 0.0001
    }

    resp = send_generic_post_requests(buy_url, data_buy_information)
    resp = json.loads(resp)
    print(resp)
    return resp


def cancel_order(uid):
    order_url = "http://cis2016-exchange1.herokuapp.com/api/orders/{uid}?next_stage".format(uid=uid)

    data_buy_information = {
        "team_uid": "WQKW1pUQiKdCw7TIzBnWwg",
        'id': uid
    }

    jsondata = json.dumps(data_buy_information)
    postreq = urllib2.Request(order_url, jsondata)
    postreq.get_method = lambda: 'DELETE'

    val = urllib2.urlopen(postreq).read()
    print(val)
    return val

'''
1. Buy on market
2. Sell on market
3. Buy on limit
4. Sell on limit
5. Read market data
'''

if stage == 1 :
    send_setup_request()

if stage == 2 :
    ret = test_buy_sell()
    uid = ret['id']
    print(uid)
    cancel_order(uid)