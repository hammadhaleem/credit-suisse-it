import json
import urllib2

post_fields = {
    "name": "Code-Ninja",
    "members": ['Hammad Haleem', 'Vikram Sambamurty', 'Irtaza Khan']
}

url = "http://cis2016-teamtracker.herokuapp.com/api/teams"


def send_setup_request():
    jsondata = json.dumps(post_fields)
    postreq = urllib2.Request(url, jsondata)
    postreq.add_header('Content-Type', 'application/json')
    resp = urllib2.urlopen(postreq).read()
    print(resp)
    return resp

send_setup_request()