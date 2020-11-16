# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function

from flask import request, g

from . import Resource
from .. import schemas
import hashlib
from timeslot.timeslot.v1.Booking import Booking
import json

class Bookings(Resource):

    def get(self):
        print(g.args)
        

        return {}, 200, None

    def post(self):
        dentistName = str(request.json['dentistName'])
        time = int(request.json['time'])
        patientName = str(request.json['patientName'])
        id = generate_hash_id(dentistName, time, patientName)
        booking = Booking(id, dentistName, time, patientName)

        all_bookings = Booking.read_from_file()
        all_bookings['bookings'].append(booking.values())
        Booking.write_to_file(all_bookings)

        resp = {'id': id}
        return resp, 201, None

def generate_hash_id(dentistName: str, time: int, patientName: str):
    s = dentistName + str(time) + patientName
    return hashlib.md5(s.encode('utf-8')).hexdigest()[1:6]

def read_from_file():
    fname = 'bookings.json'
    with open(fname, "r") as books:
        return json.loads(books.read())