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
        arguments = g.args
        dentistName, time, patientName = fetch_params_from_arg(arguments)
        all_bookings = Booking.read_from_file()
        all_bookings = all_bookings['bookings']

        if dentistName:
            all_bookings = get_by_dentistName(all_bookings, dentistName)
        if time:
            all_bookings = get_by_time(all_bookings, time)
        if patientName:
            all_bookings = get_by_patientName(all_bookings, patientName)

        resp = {'data': all_bookings}
        return resp, 200, None

    def post(self):
        dentistName = str(request.json['dentistName'])
        time = request.json['time']
        patientName = str(request.json['patientName'])
        id = generate_hash_id(dentistName, time, patientName)
        booking = Booking(id, dentistName, time, patientName)

        all_bookings = Booking.read_from_file()
        all_bookings['bookings'].append(booking.values())
        Booking.write_to_file(all_bookings)

        resp = {'id': id}
        return resp, 201, None


def fetch_params_from_arg(arguments):
    dentistName = arguments.get('dentistName')
    time = arguments.get('time')
    patientName = arguments.get('patientName')

    return dentistName, time, patientName


def get_by_dentistName(all_bookings: list, dentistName: str):
    vals = list()
    for booking in all_bookings:
        if booking['dentistName'] == dentistName:
            vals.append(booking)
    return vals


def get_by_time(all_bookings: list, time: int):
    vals = list()
    for booking in all_bookings:
        if booking['time'] == time:
            vals.append(booking)
    return vals


def get_by_patientName(all_bookings: list, patientName: str):
    vals = list()
    for booking in all_bookings:
        if booking['patientName'] == patientName:
            vals.append(booking)
    return vals


def generate_hash_id(dentistName: str, time: str, patientName: str):
    s = dentistName + time + patientName
    s = hashlib.md5(s.encode('utf-8')).hexdigest()
    s = s[:5]
    return s