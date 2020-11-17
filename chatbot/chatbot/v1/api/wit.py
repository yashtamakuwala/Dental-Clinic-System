from .credentials import WIT_TOKEN
import requests, json
from flask_restful import current_app
from .Dentist import Dentist
from .Patient import Patient
from .Booking import Booking
from .Timeslot import Timeslot

dentist = Dentist()
booking = Booking()
timeslot = Timeslot()


def ask_wit(expression: str, patient: Patient):
    ep = 'https://api.wit.ai/message?v=20201117&q={}'.format(expression)
    headers = {'Authorization': WIT_TOKEN}

    result = requests.get(ep, headers=headers)
    result = result.json()

    try:
        ans = answer_greeting(result)
        if ans:
            patient.hiDone = True
            return ans

        ans = check_get_intents(result, patient)
        if ans:
            return ans

    except KeyError as error:
        ans = 'Cant comprehend'
    return ans


def ans_dentist(dentistData: list):
    ans = str()
    if len(dentistData) == 1:
        result = dentistData[0]
        ans = f"Dentist {result['name']} specialises in {result['specialisation']} and is located at {result['location']}."
        return ans, result['id']

        # TODO: handle not found
        # else:
        #     ans = f"Dentist by the name {name} not found. Please check your details."
        #     return ans
    # Searching for ALL dentists
    else:
        for den in dentistData:
            ans += f" {den['name']}, "
        ans = ans[:-2]
        ans = f"Dentists {ans} are available."
        return ans, None


def answer_greeting(result: dict):
    traits = result['traits']
    ans = None
    if traits:
        if 'wit$greetings' in traits.keys():
            ans = 'Hi. Its a great day. How may I assist you?'
    return ans


def check_get_intents(result: dict, patient: Patient):
    GET_DENTISTS_INTENT = "getDentists"
    GET_NAME_INTENT = "name"

    intents = result['intents']
    ans = None
    name = None
    for intent in intents:
        intentName = intent['name']

        if intentName == GET_DENTISTS_INTENT:
            allDentists = dentist.get_all_dentists(name=None)
            # TODO: check for their time availability
            allDentists = available_dentists(allDentists)
            ans, id = ans_dentist(allDentists)
            patient.getAllDentists = True

        #  Patient name available so this name is doctor name
        if intentName == GET_NAME_INTENT and patient.name:
            name = get_dentist_name(result['entities'])
            result = dentist.get_all_dentists(name)
            if result:
                ans, id = ans_dentist(result)

            else:
                ans = f'Dentist by the name {name} not found.'

    return ans


def available_dentists(allDentists: list) -> list:
    validHours = len(timeslot.get_all_timeslots())
    av_dentists = list()
    for i, dent in enumerate(allDentists):
        name = dent['name']
        bookings = booking.get_bookings(name, None, None)

        if len(bookings) < validHours:
            av_dentists.append(dent)
    return av_dentists


def get_dentist_name(entities: dict):
    name = None
    contact = entities['wit$contact:contact']
    name = contact[0]['value']
    return name
