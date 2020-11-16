import json


class Booking:
    def __init__(self, id:str, dentistName: str, time: int, patientName: str):
        self.id = id
        self.dentistName = dentistName
        self.time = time
        self.patientName = patientName

    def values(self):
        return {'id': self.id, 'dentistName': self.dentistName, 'time': self.time, 'patientName': self.patientName}

    def read_from_file():
        fname = 'bookings.json'
        with open(fname, "r") as books:
            return json.loads(books.read())

    def write_to_file(content):
        fname = 'bookings.json'
        with open(fname, "w") as bookings:
            bookings.write(json.dumps(content))
