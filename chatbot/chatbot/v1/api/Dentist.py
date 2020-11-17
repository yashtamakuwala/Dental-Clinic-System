import requests

DENT_SERVER = 'http://127.0.0.1'
DENT_PORT = '7000'
GET_DENTISTS = '/v1/dentists'
GET_DENTIST_BY_ID = '/v1/'


class Dentist:
    def get_all_dentists(self, name: str):
        ep = DENT_SERVER + ':' + DENT_PORT + GET_DENTISTS
        if name:
            ep = ep + '?name=' + name

        result = requests.get(ep)
        result = result.json()
        result = result["data"]
        return result
