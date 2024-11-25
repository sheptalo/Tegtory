from requests import get
from dotenv import load_dotenv
from os import environ
from bot import api

load_dotenv()
api_url = environ.get("API_URL") + "api/v1/"


class Leaderboard:
    class Money:
        def __init__(self):
            self.url = f"{api_url}leaderboard/money"

        def __str__(self):
            return get(self.url, headers=api.headers).json()

        def me(self, iternal_id):
            return get(f"{self.url}/{iternal_id}", headers=api.headers).json()

    class Stolar:
        def __init__(self):
            self.url = f"{api_url}leaderboard/stolar"

        def __str__(self):
            return get(self.url, headers=api.headers).json()

        def me(self, iternal_id):
            return get(f"{self.url}/{iternal_id}", headers=api.headers).json()

    class Rating:
        def __init__(self):
            self.url = f"{api_url}leaderboard/rating"

        def __str__(self):
            return get(self.url, headers=api.headers).json()

        def me(self, iternal_id):
            return get(f"{self.url}/{iternal_id}", headers=api.headers).json()

    class Level:
        def __init__(self):
            self.url = f"{api_url}leaderboard/level"

        def __str__(self):
            return get(self.url, headers=api.headers).json().replace("_", "\\_")

        def me(self, iternal_id):
            return get(f"{self.url}/{iternal_id}", headers=api.headers).json()

    class Eco:
        def __init__(self):
            self.url = f"{api_url}leaderboard/ecology"

        def __str__(self):
            return get(self.url, headers=api.headers).json().replace("_", "\\_")

        def me(self, iternal_id):
            return get(f"{self.url}/{iternal_id}", headers=api.headers).json()

    class Clan:
        def __init__(self, name):
            self.clan_name = name

        def __str__(self):
            return get(
                f"{api_url}leaderboard/clans/{self.clan_name}", headers=api.headers
            ).json()

    class Clans:
        def __str__(self):
            return get(f"{api_url}leaderboard/clans", headers=api.headers).json()
