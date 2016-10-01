import requests

register_dict = {
    "id":16,
    "name":"CodeNinja",
    "members":"[\"Kelvin\", \"Wing\", \"Jay\", \"Matthew\"]",
}

url = "http://cis2016-teamtracker.herokuapp.com/api/teams"


def send_setup_request():

    r = requests.post(url, data=register_dict)
    print(r.status_code, r.reason)


send_setup_request