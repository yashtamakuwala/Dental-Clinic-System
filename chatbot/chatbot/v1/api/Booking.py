import requests

TIME_SERVER= 'http://127.0.0.1:'
TIME_PORT = '8000'
GET_BOOKINGS = POST_BOOKINGS = '/v1/bookings'


class Booking:
    def get_bookings(self, dentistName: str, time: str, patientName: str) -> list:
        ep = TIME_SERVER + TIME_PORT + GET_BOOKINGS
        params = build_params(dentistName, time, patientName)

        result = requests.get(ep, params=params)
        if result.status_code == 200:
            result = result.json()
            return result['data']
        else:
            return None

    def add_booking(self, dentistName: str, time: str, patientName: str) -> int:
        ep = TIME_SERVER + TIME_PORT + POST_BOOKINGS
        body = build_params(dentistName, time, patientName)

        result = requests.post(ep, json=body)


        if result.status_code == 201:
            result = result.json()
            id = result['id']
            return id
        else:
            return None

    def delete_booking(self, id):
        ep = ep = TIME_SERVER + TIME_PORT + GET_BOOKINGS + '/' + str(id)
        result = requests.delete(ep)

        if result.status_code == 204:
            return True
        else:
            return False

def build_params(dentistName: str, time: str, patientName: str):
    params = {}
    if dentistName:
        params['dentistName'] = dentistName
    if time:
        params['time'] = time
    if patientName:
        params['patientName'] = patientName
    return params