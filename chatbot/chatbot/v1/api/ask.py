# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function

from flask import request, g, current_app

from . import Resource
from .. import schemas
from .wit import ask_wit
from .Patient import Patient


class Ask(Resource):

    def get(self):
        expression = g.args.get('message')
        patientName = g.args.get('patient')

        patients = current_app.patients
        isFound = False
        patient = None

        if patients:
            for pat in patients:
                if patientName:
                    if pat.name == patientName:
                        isFound = True
                        patient = pat

        if not isFound:
            patient = Patient()
            patients.append(patient)

        ans, name = ask_wit(expression, patient)
        if not name:
            del patient

        resp = {'answer': ans, 'name': name}
        return resp, 200, None
