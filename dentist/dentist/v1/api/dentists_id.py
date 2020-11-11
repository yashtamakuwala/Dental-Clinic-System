# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function

from flask import request, g

from . import Resource
from .. import schemas
import json

class DentistsId(Resource):

    def get(self, id):
        dentists = read_from_file()
        dentists = dentists['dentists']
        for dentist in dentists:
            if dentist["id"] == id:
                return dentist, 200, None
        return 404, None


def read_from_file():
    fname = 'dentist_data.json'
    with open(fname, "r") as books:
        return json.loads(books.read())