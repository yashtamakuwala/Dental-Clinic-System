DENT_SERVER = 'http://127.0.0.1'
DENT_PORT = '7000'
GET_DENTISTS = '/v1/dentists'
GET_DENTIST_BY_ID = '/v1/'

import requests

class Dentist:
    def get_all_dentists(name: str):

        ep = DENT_SERVER + ':' + DENT_PORT + GET_DENTISTS
        if name:
            ep = ep + '?name=' + name

        result = requests.get(ep)
        result = result.json()
        ans = str()
        result = result["data"]
        return result

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

    # def get_dentisit_by_id(self, id: int):
