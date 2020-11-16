from .credentials import WIT_TOKEN
import requests
from flask_restful import current_app

DENT_SERVER = 'http://127.0.0.1'
DENT_PORT = '7000'
DENT_PATH = '/v1/dentists'

def ask_wit(expression: str):
    ep = 'https://api.wit.ai/message?v=20201112&q={}'.format(expression)
    headers = {'Authorization': WIT_TOKEN}

    result = requests.get(ep, headers= headers)
    result = result.json()

    try:
        ans = answer_greeting(result)
        if ans:
            return ans

        ans = check_get_intents(result)
        if ans:
            return ans

        name = result['intents'][0]['name']
        location = result['entities']['wit$location:location'][0]['resolved']['values'][0]['name']
        print(f'Location is : {location}')
        if name == 'GetWeatherForecast':
            ans = get_weather_forecast(location)
        elif name == 'FindRestaurant':
            cuisine = result['entities']['cuisine:cuisine'][0]['value']
            ans = get_restaurants(location, cuisine)
    except KeyError as error:
        ans = 'Cant comprehend'
    return ans

def answer_greeting(result: dict):
    traits = result['traits']
    ans = None
    if traits:
        if 'wit$greetings' in traits.keys():
            ans = 'Hi. Its a great day. How are you?'
    return ans

def check_get_intents(result: dict):
    GET_DENTISTS_INTENT = "getDentists"
    GET_NAME_INTENT = "dentistName"
    intents = result['intents']
    isGetDentists = False
    isGetName = False
    ans = None
    name = None
    for intent in intents:
        if intent['name'] == GET_DENTISTS_INTENT:
            isGetDentists = True
        if intent["name"] == GET_NAME_INTENT:
            isGetName = True
            name = get_dentist_name(result['entities'])
            break

    if isGetDentists or isGetName:
        ans = get_all_dentists(name)
    return ans

def get_dentist_name(entities:dict):
    name = None
    contact = entities['wit$contact:contact']
    name = contact[0]['value']
    return name

def get_all_dentists(name: str):

    ep = DENT_SERVER + ':' + DENT_PORT + DENT_PATH
    if name:
        ep = ep + '?name=' + name

    result = requests.get(ep)
    result = result.json()
    ans = str()
    result = result["data"]

    # Searching for 1 dentist
    if name:
        if result:
            result = result[0]
            ans = f"Dr. {name} specialises in {result['specialisation']} and is located at {result['location']}."
            current_app.name = name
            current_app.id = result['id']
            return ans
        else:
            ans = f"Dentist by the name {name} not found. Please check your details."
            return ans
    # Searching for ALL dentists
    else:
        if result:
            for den in result:
                ans += f"Dr. {den['name']}, "
            ans = ans[:-2]
            return f"Dentists {ans} are available."