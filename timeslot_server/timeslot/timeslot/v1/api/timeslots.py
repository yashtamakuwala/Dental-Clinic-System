# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function

from flask import request, g

from . import Resource
from .. import schemas
import json


class Timeslots(Resource):

    def get(self):
        timeslots = read_from_file()
        data = timeslots['timeslots']
        resp = {'data': data}
        return resp, 200, None


def read_from_file():
    fname = 'valid_timeslots.json'
    with open(fname, "r") as books:
        return json.loads(books.read())