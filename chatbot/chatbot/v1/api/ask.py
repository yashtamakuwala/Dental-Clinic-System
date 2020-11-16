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
        if patientName in patients:
            patient = patients[patientName]

        else:  # add a patient
            patients[patientName] = Patient(patientName)
            patient = patients[patientName]
            current_app.patients = patients

        ans = ask_wit(expression, patient)
        resp = {'answer': ans}
        return resp, 200, None
