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
    print(resp)
    return resp


def test_buy_sell():
    buy_url = "http://cis2016-exchange1.herokuapp.com/api/orders/"
    data_buy_information = {
        "symbol": "0005",
        'side' : "sell",
        'qty' : 1,
        "team_uid":"WQKW1pUQiKdCw7TIzBnWwg",
        'order_type' : 'market'
    }

    resp = send_generic_post_requests(buy_url, data_buy_information)
    print(resp)
    return resp

if stage == 1 :
    send_setup_request()

if stage == 2 :
    test_buy_sell()