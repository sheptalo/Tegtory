from requests import get
from dotenv import load_dotenv
from os import environ
from api import api

load_dotenv()
api_url = environ.get('API_URL')


class Leaderboard:
    class Money:
        def __init__(self):
            self.url = f'{api_url}/api/v1/leaderboard/money'

        def __str__(self):
            return eval(get(self.url, headers=api.headers).text)

        def me(self, iternal_id):
            return eval(get(f'{self.url}/{iternal_id}', headers=api.headers).text)

    class Stolar:
        def __init__(self):
            self.url = f'{api_url}/api/v1/leaderboard/stolar'

        def __str__(self):
            return eval(get(self.url, headers=api.headers).text)

        def me(self, iternal_id):
            return eval(get(f'{self.url}/{iternal_id}', headers=api.headers).text)

    class Rating:
        def __init__(self):
            self.url = f'{api_url}/api/v1/leaderboard/rating'

        def __str__(self):
            return eval(get(self.url, headers=api.headers).text)

        def me(self, iternal_id):
            return eval(get(f'{self.url}/{iternal_id}', headers=api.headers).text)

    class Level:
        def __init__(self):
            self.url = f'{api_url}/api/v1/leaderboard/level'

        def __str__(self):
            return eval(get(self.url, headers=api.headers).text)

        def me(self, iternal_id):
            return eval(get(f'{self.url}/{iternal_id}', headers=api.headers).text)

    class Eco:
        def __init__(self):
            self.url = f'{api_url}/api/v1/leaderboard/ecology'

        def __str__(self):
            return eval(get(self.url, headers=api.headers).text)

        def me(self, iternal_id):
            return eval(get(f'{self.url}/{iternal_id}', headers=api.headers).text)

    class Clan:
        def __init__(self, name):
            self.clan_name = name

        def __str__(self):
            return eval(get(f'{api_url}/api/v1/leaderboard/clans/{self.clan_name}', headers=api.headers).text)

    class Clans:
        def __str__(self):
            return eval(get(f'{api_url}/api/v1/leaderboard/clans', headers=api.headers).text)
