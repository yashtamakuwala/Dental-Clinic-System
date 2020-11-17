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
        ans = answer_greeting(result, patient.name)
        if ans:
            patient.hiDone = True
        # return ans

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
        ans = f"Dentist {result['name']} specialises in {result['specialisation']} and is located at {result['location']}. " \
              f"When would you like an appointment?"
        return ans, result['id']

    else:
        for den in dentistData:
            ans += f" {den['name']}, "
        ans = ans[:-2]
        ans = f"Dentists {ans} are available."
        return ans, None


def answer_greeting(result: dict, name: str):
    traits = result['traits']
    ans = None
    if traits:
        if 'wit$greetings' in traits.keys():
            if name:
                ans += f'Hi {name}. Its a great day. How may I assist you?'
            else:
                ans = 'Hi, Hope you are well. Whats your name?'
    return ans


def check_get_intents(result: dict, patient: Patient):
    GET_DENTISTS_INTENT = "getDentists"
    GET_NAME_INTENT = "name"
    TIME_SELECTED = 'timeSelected'
    CONFIRMATION = 'confirmation'

    intents = result['intents']
    ans = None
    name = None
    for intent in intents:
        intentName = intent['name']

        if intentName == GET_NAME_INTENT and not patient.name:
            name = get_name(result['entities'])
            patient.set_patient_name(name)
            break

        if intentName == GET_DENTISTS_INTENT:
            allDentists = dentist.get_all_dentists(name=None)
            allDentists = available_dentists(allDentists)
            ans, id = ans_dentist(allDentists)
            patient.shown_dentists()
            break

        #  Patient name available so this name is doctor name
        if intentName == GET_NAME_INTENT and patient.name and not patient.dentistName:
            name = get_name(result['entities'])
            result = dentist.get_all_dentists(name)
            if result:
                ans, id = ans_dentist(result)
                patient.got_dentist_name(result[0]['name'])
            else:
                ans = f'Dentist by the name {name} not found.'
            break

        # Patient has selected doctor and asking for appointment at a particular time
        if patient.dentistName and intentName == TIME_SELECTED:
            witTime = result['entities']['wit$datetime:datetime'][0]
            hh, mm = time_entity(witTime)
            # TODO: check the 24 hr time values
            ans = time_selected_response(hh, patient)

        if patient.time and patient.dentistName and intentName == CONFIRMATION:
            ans = confirmation(result['entities']['confirmation:confirmation'], patient)

    return ans


def confirmation(confirmDict: dict, patient: Patient):
    value = confirmDict['value']
    value = value == 'yes'

    # Yes, book appointment
    if value:
        patient.confirmation = True
        bId = booking.add_booking(dentistName=patient.dentistName, time=patient.time,
                                  patientName=patient.name)
        if bId:
            ans = f'Hey {patient.name} your booking with Dr. {patient.dentistName}' \
                  f'at {patient.time} has been confirmed. ' \
                  f'Your booking id is {bId}. ' \
                  f'See you tomorrow at {patient.time}.'
            patient.confirm_appointment()
        else:
            ans = 'Could not book. Please check your details and try again'
    else:
        ans = 'Okay. You could book for another time.' \
              ' Alternatively, I can also show you all available dentists.'
        patient.decline_appointment()
    return ans


def time_selected_response(hh: str, patient: Patient) -> str:
    hh = str(hh if hh < 16 else hh - 12)
    ans = None
    result = booking.get_bookings(dentistName=patient.dentistName,
                                  time=hh, patientName=None)

    # if found then dentist already booked for that hour
    # ans suggest alternate timeslots
    if result:
        altHours = alternate_timeslots(hh=hh)
        ans = f'Dr. {patient.dentistName} is booked at {hh}. ' \
              f'Here are alternate 1 hr timeslots you might want to book for.' \
              f'You can book from - {altHours}'

    else:
        ans = f'Dr. {patient.dentistName} is available at {hh}. ' \
              f'Do you want to book it?'
    patient.asked_appointment_time(hh)
    return ans


def alternate_timeslots(hh: str):
    validHours = timeslot.get_all_timeslots()
    validHours = set(validHours.split(','))
    validHours = validHours.difference({hh})
    validHours = ' '.join(validHours)
    return validHours


def time_entity(witTime: dict) -> (int, int):
    value = witTime['value']
    # 2020-11-17T04:00:00.000-08:00

    value = value.split('T')[1]
    # 04:00:00.000-08:00
    value = value.split(':')
    hh, mm = int(value[0]), int(value[1])
    return hh, mm


def available_dentists(allDentists: list) -> list:
    validHours = timeslot.get_all_timeslots()
    validHours = len(validHours.split(','))
    av_dentists = list()
    for i, dent in enumerate(allDentists):
        name = dent['name']
        bookings = booking.get_bookings(name, None, None)

        if len(bookings) < validHours:
            av_dentists.append(dent)
    return av_dentists


def get_name(entities: dict):
    name = None
    contact = entities['wit$contact:contact']
    name = contact[0]['value']
    return name
