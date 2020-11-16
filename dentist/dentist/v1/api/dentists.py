# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function

from flask import request, g

from . import Resource
from .. import schemas
import json


class Dentists(Resource):

    def get(self):
        dentists = read_from_file()
        dentists = dentists["data"]

        args = request.args
        name = str()
        if args:
            name = args.get('name')
            data = list()
            for dentist in dentists:
                if dentist["name"] == name:
                    data.append(dentist)
                    resp = {'data': data}
                    return resp, 200, None
            resp = {'data': data}
            if data:
                return resp, 200, None

            #     Not Found
            else:
                return 404, None

        resp = {'data': dentists}
        return resp, 200, None


def read_from_file():
    fname = 'dentist_data.json'
    with open(fname, "r") as books:
        return json.loads(books.read())
