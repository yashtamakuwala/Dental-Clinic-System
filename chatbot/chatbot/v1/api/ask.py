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
                        break

        if not isFound:
            patient = Patient()
            patients.append(patient)

        res = ask_wit(expression, patient)
        if res:
            ans, name = res[0], res[1]
        else:
            ans, name = "What's your good name?", ''
        delete_noname_patients()

        resp = {'answer': ans, 'name': name}
        return resp, 200, None


def delete_noname_patients():
    patients = current_app.patients
    newP = list()
    for pat in patients:
        if pat.name:
            newP.append(pat)
    current_app.patients = newP
