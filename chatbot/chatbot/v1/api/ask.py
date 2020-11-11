# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function

from flask import request, g

from . import Resource
from .. import schemas
from .wit import ask_wit

class Ask(Resource):

    def get(self):
        expression = g.args.get('message')
        ans = ask_wit(expression)
        resp = {'answer': ans}
        return resp, 200, None