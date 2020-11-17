import requests

TIME_SERVER= 'http://127.0.0.1:'
TIME_PORT = '8000'
GET_TIMES = '/v1/timeslots'


class Timeslot:
    def get_all_timeslots(self) -> str:
        ep = TIME_SERVER + TIME_PORT + GET_TIMES
        result = requests.get(ep)
        result = result.json()
        result = result['data']
        return result
