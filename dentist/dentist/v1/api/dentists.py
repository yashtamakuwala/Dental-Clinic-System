# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function

from flask import request, g

from . import Resource
from .. import schemas
import json

class Dentists(Resource):

    def get(self):
        dentists = read_from_file()
        dentists = dentists["dentists"]
        resp = {'data': dentists}

        return dentists, 200, None

def read_from_file():
    fname = 'dentist_data.json'
    with open(fname, "r") as books:
        return json.loads(books.read())