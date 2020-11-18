# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function

from flask import request, g

from . import Resource
from .. import schemas
from ..Booking import Booking

class BookingsId(Resource):

    def delete(self, id):
        all_bookings = Booking.read_from_file()
        all_bookings = all_bookings['bookings']

        new_bookings = list()
        for appoint in all_bookings:
            if not appoint['id'] == id:
                new_bookings.append(appoint)

        d = {'bookings': new_bookings}
        Booking.write_to_file(d)

        return None, 204, None