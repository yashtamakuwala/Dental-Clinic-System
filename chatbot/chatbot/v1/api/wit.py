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

        ans2, name = check_get_intents(result, patient)
        if not ans2 and name:
            patient.hiDone = True
            return (f'Hi {name}', name)
        else:
            if not patient.hiDone:
                ans = answer_greeting(result, patient.name)
                if ans:
                    patient.hiDone = True
                    return ans, ''
            else:
                return ans2, name

    except KeyError as error:
        ans = 'Could not process. Whats your good name?', ''
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
    CANCELLATION = 'cancel'

    intents = result['intents']
    ans = None
    name = patient.name if patient else None
    for intent in intents:
        intentName = intent['name']

        if intentName == GET_NAME_INTENT and not patient.name and not patient.wantingToCancel:
            name = get_name(result['entities'])
            patient.set_patient_name(name)
            break

        if intentName == GET_DENTISTS_INTENT:
            allDentists = dentist.get_all_dentists(name=None)
            allDentists = available_dentists(allDentists)
            ans, id = ans_dentist(allDentists)
            if ans:
                patient.shown_dentists()
            else:
                ans = 'No dentists are available. Please try again later.'
            break

        #  Patient name available so this name is doctor name
        if intentName == GET_NAME_INTENT \
                and patient.name and not patient.dentistName \
                and not patient.wantingToCancel:
            dentName = get_name(result['entities'])
            result = dentist.get_all_dentists(dentName)
            if result:
                ans, id = ans_dentist(result)
                patient.got_dentist_name(result[0]['name'])
            else:
                ans = f'Dentist by the name {dentName} not found.'
            break

        # Patient has selected doctor and asking for appointment at a particular time
        if patient.dentistName and intentName == TIME_SELECTED \
                and not patient.cancelTime:
            witTime = result['entities']['wit$datetime:datetime'][0]
            hh, mm = time_entity(witTime)
            # TODO: check the 24 hr time values
            ans = time_selected_response(hh, patient)

        # Ask for confirmation of booking
        if patient.time and patient.dentistName and intentName == CONFIRMATION:
            ans = confirmation(result['entities']['confirmation:confirmation'][0], patient)

        # Requested to cancel
        if patient.name and intentName == CANCELLATION \
                and not patient.dentistName and not patient.cancelTime:
            ans = get_bookings_to_cancel(patient)
            break

        # get all bookings to cancel and ask by dentist name
        if patient.name and intentName == GET_NAME_INTENT \
                and patient.wantingToCancel:
            cancelDentist = get_name(entities=result['entities'])
            ans = cancel_dentist_response(cancelDentist, patient)
            break

        # get bookings and time of appointment to cancel
        if patient.name and patient.wantingToCancel and patient.cancelDentist \
                and not patient.cancelTime:
            witTime = result['entities']['wit$datetime:datetime'][0]
            hh, mm = time_entity(witTime)
            # TODO: check the 24 hr time values
            ans = cancel_time_response(hh, patient)
            break

        # Got cancel details and now confirmation to cancel
        if patient.name and patient.wantingToCancel and \
                patient.cancelDentist and patient.cancelTime and intentName == CONFIRMATION:
            ans = confirm_cancel(result['entities']['confirmation:confirmation'][0], patient)

    return ans, name


def cancel_time_response(hh: str, patient: Patient):
    result = booking.get_bookings(dentistName=patient.cancelDentist, time=hh,
                                  patientName=patient.name)
    isFound = False
    for book in result:
        if book['time'] == hh:
            isFound = True
    hhDay = ans_time_string(hh)
    if result:
        patient.cancelTime = hh

        ans = f"Are you sure you want to cancel " \
              f"your booking with {patient.cancelDentist} at {hhDay}"
    else:
        ans = f'Booking at time {hhDay} not found. Please check time.'
    return ans


def cancel_dentist_response(cancelDentist: str, patient: Patient):
    result = dentist.get_all_dentists(cancelDentist)
    if result:
        patient.cancelDentist = cancelDentist
        result = booking.get_bookings(dentistName=cancelDentist, time=None,
                                      patientName=patient.name)
        if result:
            t = str()
            for app in result:
                t += str(ans_time_string(app['time'])) + ', '
            t = t[:-2]
            ans = f'you have appointment(s) with {cancelDentist} at {t}. Select time you want to cancel.'
    else:
        ans = f'Dentist by the name {cancelDentist} not found.'
    return ans


def get_bookings_to_cancel(patient: Patient):
    patient.wantingToCancel = True
    allBookings = booking.get_bookings(dentistName=None, time=None, patientName=patient.name)
    ans = str()

    if allBookings:
        for appoint in allBookings:
            ans += str(ans_time_string(appoint['time'])) + f" with dentist {appoint['dentistName']}" + ', '
        ans = ans[:-2]
    ans = f'You have booking(s) at {ans}. Enter dentist whose booking you wish to cancel.'
    return ans


def confirm_cancel(confirmDict: dict, patient: Patient):
    value = confirmDict['value']
    value = value == 'yes'

    # yes, cancel booking
    if value:
        res = booking.get_bookings(dentistName=patient.cancelDentist, time=patient.cancelTime,
                                   patientName=patient.name)
        if res:
            bId = res[0]['id']
            res = booking.delete_booking(bId)
            if res:
                ans = f'Booking deleted. How else can I assist you {patient.name}'
                patient.booking_cancelled()
            else:
                ans = 'Please try again.'
        else:
            return 'Please check details.'
    else:
        ans = 'Okay. How else may I assist you?'
    return ans



def confirmation(confirmDict: dict, patient: Patient):
    value = confirmDict['value']
    value = value == 'yes'

    # Yes, book booking
    if value:
        patient.confirmation = True
        res = booking.get_bookings(dentistName=None, time=patient.time,
                                   patientName=patient.name)

        if res:
            ans = 'You already have a booking at that time. ' \
                  'Please select an alternate booking time.'
            return ans

        bId = booking.add_booking(dentistName=patient.dentistName, time=patient.time,
                                  patientName=patient.name)
        if bId:
            ans = f'Hey {patient.name}, your booking with Dr. {patient.dentistName} ' \
                  f'at {patient.time} has been confirmed. ' \
                  f'Your booking id is {bId}. ' \
                  f'See you tomorrow at {patient.time}.'
            patient.confirm_appointment(bId)
        else:
            ans = 'Could not book. Please check your details and try again'
    else:
        ans = 'Okay. You could book for another time.' \
              ' Alternatively, I can also show you all available dentists.'
        patient.decline_appointment()
    return ans

# can take hh of 24hr time system
def ans_time_string(hh: str):
    day = 'am'
    hhInt = int(hh)
    if hhInt == 12:
        day = 'pm'
    elif hhInt > 12:
        day = 'pm'
        hhInt -= 12
    else:
        day = 'am'
    return f'{str(hhInt)}{day}'

def time_selected_response(hh: str, patient: Patient) -> str:
    hh = str(hh)
    validHours = timeslot.get_all_timeslots().split(',')
    # test_list = [int(i) for i in test_list]
    if hh not in validHours:
        ans = f'Invalid time. Please try alternate time format or {alternate_timeslots(hh)}.'
        return ans

    ans = None
    hh = ans_time_string(hh)
    result = booking.get_bookings(dentistName=patient.dentistName,
                                  time=hh, patientName=None)

    # if found then dentist already booked for that hour
    # ans suggest alternate timeslots
    if result:
        altHours = alternate_timeslots(hh=hh)
        ans = f'Dr. {patient.dentistName} is booked at {hh}. ' \
              f'Here are alternate 1 hr timeslots you might want to book for. ' \
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
    validHours = list(validHours)
    validHours.sort()
    validHours = ' ,'.join(validHours)
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
