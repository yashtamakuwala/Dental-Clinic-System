from .credentials import WIT_TOKEN
import requests

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
            ans = 'Hi, How are you?'
    return ans

def check_get_intents(result: dict):
    GET_DENTISTS_INTENT = "getDentists"
    GET_NAME_INTENT = "dentistName"
    intents = result['intents']
    isGetDentists = False
    isGetName = False
    ans = None
    for intent in intents:
        if intent['name'] == GET_DENTISTS_INTENT:
            isGetDentists = True
            break
        elif intent["name"] == GET_NAME_INTENT:
            isGetName = True
            break

    if isGetDentists or isGetName:
        ans = get_all_dentists()
    if
    return ans

def get_all_dentists(name: str):
    server = 'http://127.0.0.1:7000'
    path = '/v1/dentists'
    if name:
        path = path + '?name=' + name
    result = requests.get(server+path)
    result = result.json()
    print(result)
    return str(result)
