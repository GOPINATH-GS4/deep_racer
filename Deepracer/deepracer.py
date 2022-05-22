import json
from requests_html import HTMLSession
import random

class Deepracer:
    def __init__(self, base_url: str, password: str):
        self.__password = password
        self.__base_url = base_url
        self.__login_url = f'{base_url}/login'
        self.__set_led_color_url = f'{base_url}/api/set_led_color'
        self.__get_led_color_url = f'{base_url}/api/get_led_color'
        self.__get_battery_level_url = f'{base_url}/api/get_battery_level'
        self.__cookies = None
        self.__session_token = None

    def __get_csrf_token(self):
        self.__session = HTMLSession()
        self.__session.verify = False
        r = self.__session.get(self.__login_url)
        meta_tags = r.html.find('meta')
        self.__cookies = r.cookies
        self.__csrf_tokens = [meta.attrs['content'] for meta in meta_tags if meta.attrs['name'] == 'csrf-token']

    def login(self):
        self.__get_csrf_token()

        if len(self.__csrf_tokens) <= 0 or len(self.__cookies) <= 0:
            raise Exception("Unable to obtain csrf-token or session cookie")
        self.__session_token = self.__cookies.get_dict()['session']
        data = dict()
        headers = dict()
        data['password'] = self.__password
        headers['Content-Type'] = 'application/x-www-form-urlencoded'
        headers['Cookie'] = f'session={self.__session_token}'
        headers['X-CSRFToken'] = self.__csrf_tokens[0]
        response = self.__session.post(self.__login_url, headers=headers, data=data, verify=False)

        if response.status_code != 200:
            print(f'Unable to login {response.text}')
            return False
        self.__cookies = response.cookies
        return True

    def ___make_header(self):
        headers = dict()
        headers['Content-Type'] = 'application/json'
        headers['X-CSRF-Token'] = self.__csrf_tokens[0]
        headers[
            'Cookie'] = f'session={self.__session_token}; deepracer_token={self.__cookies.get_dict()["deepracer_token"]}'
        return headers

    def __set_lead_color(self, r, g, b):
        data = {"red": r, "green": g, "blue": b}
        response = self.__session.post(self.__set_led_color_url, headers=self.___make_header(), json=data,
                                       cookies=self.__cookies,
                                       verify=False)
        if response.status_code != 200:
            print(f'Unable to set the LED COLOR {response.text}')
            return False
        return True

    def set_led_color(self, r, g, b, rand=False):
        if rand:
            return self.__set_lead_color(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        else:
            return self.__set_lead_color(r, g, b)

    def get_led_color(self):
        response = self.__session.get(self.__get_led_color_url, headers=self.___make_header(), cookies=self.__cookies,
                                      verify=False)
        if response.status_code != 200:
            print(f'Unable to get the LED COLOR {response.text}')
            return json.dumps(response)
        return json.loads(response.text)

    def get_battery_level(self):
        response = self.__session.get(self.__get_battery_level_url, headers=self.___make_header___make_header(), cookies=self.__cookies,
                                      verify=False)
        if response.status_code != 200:
            print(f'Unable to get the LED COLOR {response.text}')
            return json.dumps(response)
        return json.loads(response.text)