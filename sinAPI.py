from requests import get, post
from dotenv import load_dotenv
from os import environ
from mysql.connector import connect

load_dotenv()
api_url = environ.get('API_URL')
con = connect(
        host=environ['DB_HOST'],
        port=3306,
        user=environ['USER_NAME'],
        password=environ['PASSWORD'],
        database=environ['DB_NAME'],
        autocommit=True
    )
cur = con.cursor(buffered=True)


class Base:
    def __init__(self, user_id, api_key):
        self.headers = {"Authorization": f"Bearer {api_key}"}
        self.player_id = user_id
        self.get_url = f"{api_url}/api/v1/{self.__class__.__name__}/{user_id}/"
        self.post_url = f"{api_url}/api/v1/{self.__class__.__name__}"

    def __getitem__(self, name):
        if name not in ['headers', 'player_id', 'get_url', 'post_url', 'type', 'create', 'delete', 'exists', 'exist']:
            return eval(get(self.get_url + name, headers=self.headers).text)[0]
        return self.__dict__[name]

    def __getattr__(self, name):
        if name not in ['headers', 'player_id', 'get_url', 'post_url', 'type', 'create', 'delete', 'exists', 'exist']:
            return eval(get(self.get_url + name, headers=self.headers).text, )[0]
        return self.__dict__[name]

    def __setattr__(self, name, value):
        if name not in ['headers', 'player_id', 'get_url', 'post_url', 'type', 'create', 'delete', 'exists', 'exist']:
            post(self.post_url, headers=self.headers,
                 json={"telegram_id" if self.__class__.__name__ == 'Player' else 'owner_id': self.player_id, name: value})
        else:
            self.__dict__[name] = value

    def __setitem__(self, name, value):
        if name not in ['headers', 'player_id', 'get_url', 'post_url', 'type', 'create', 'delete', 'exists', 'exist']:
            post(self.post_url, headers=self.headers,
                 json={"telegram_id" if self.__class__.__name__ == 'Player' else 'owner_id': self.player_id, name: value})
        else:
            self.__dict__[name] = value

    def global_change(self, values: dict):
        req = post(self.post_url, json=values, headers=self.headers)

    def get(self, values: str):
        return eval(get(self.get_url + values, headers=self.headers).text)


class SinApi:
    def __init__(self, api_key):
        self.api_key = api_key
        self.headers = {"Authorization": f"Bearer {self.api_key}"}

    def player(self, telegram_id):
        return self.Player(telegram_id, self.api_key)

    def factory(self, owner_id):
        return self.Factory(owner_id, self.api_key)

    def find_factory(self, name):
        req = get(f'{api_url}/api/v1/findFactory/{name}',
                  headers=self.headers).text
        return self.factory(req) if req != 0 else 0

    def stock(self):
        return eval(get(f'{api_url}/api/v1/stock',
                        headers=self.headers).text)[0]

    def stock_update(self):
        post(f'{api_url}/api/v1/stock', headers=self.headers)

    def eco_update(self):
        post(f'{api_url}/api/v1/eco', headers=self.headers)

    def league_update(self):
        post(f'{api_url}/api/v1/leagueUpdate', headers=self.headers,
             allow_redirects=True)

    def lottery_start(self):
        return eval(get(f'{api_url}/api/v1/startLottery', headers=self.headers).text)

    def reset_tickets(self):
        post(f'{api_url}/api/v1/resetTickets', headers=self.headers)

    class Player(Base):
        def __init__(self, user_id, api_key):
            try:
                int(user_id)
            except:
                user_id = get(f'{api_url}/api/v1/findUser/{user_id.replace('@', '')}',
                              headers={"Authorization": f"Bearer {api_key}"}).text
            super().__init__(user_id, api_key)

        def __str__(self):
            user_data = eval(get(self.get_url + 'name,money,stolar,rating,league,clan_name,id,titles',
                                 headers=self.headers).text)
            _text = f"""
🌟*{user_data[0]}*🌟

💲 *Баланс:* {user_data[1]:,}
⚔️ *Столар:* {user_data[2]:,}

🏆 *Рейтинг:* {user_data[3]:,}
🛡️ *Лига:* {user_data[4]}

🌎 *Oбъединение:* {user_data[5].replace('_', ' ')}

*Идентификатор*: {user_data[6]}
        """
            title = user_data[7]
            if title:
                _text += f'\n\n🏆 *Титулы:* \n'
                for name in title.split():
                    _text += f"- {name.replace('_', ' ')}\n"
            return _text

        async def create(self, username: str, user: str):
            con.ping(True)
            cur.execute("INSERT INTO"
                        " Users(telegram_id, name, league, username) VALUES (%s, %s, '', %s)",
                        (self.user_id, username, user))
            con.commit()

        @property
        def exist(self) -> bool:
            return bool(get(f'{api_url}/api/v1/exist/Player/' + str(self.player_id), headers=self.headers).text)

    class Factory(Base):
        def __init__(self, user_id, api_key):
            super().__init__(user_id, api_key)
            try:
                self.player_id = \
                    eval(get(f'{api_url}/api/v1/Player/{user_id}/id', headers=self.headers).text)[0]
            except KeyError:
                pass

        def __str__(self):
            factory_data = eval(get(self.get_url + 'name,lvl,state,tax,workers,ecology,stock,verification',
                                    headers=self.headers).text)
            return f"""
🏭 *{factory_data[0].replace('_', ' ')}*
🔧 *Уровень:* {factory_data[1]}
⚙️ *Тип:* {self.type}
🚧 *Статус:* {'Работает' if factory_data[2] == 1 else 'Не работает'}
💸 *Налоги:* {factory_data[3]}
👷‍ *Работники:* {factory_data[4]}
♻️ *Вклад в экологию:* {factory_data[5]}
📦 *Товара на складе:* {factory_data[6]}
{'🔎 _Знак качества_' if factory_data[7] == 1 else ''}
                """

        @property
        def type(self):
            lvl = self.lvl
            if lvl >= 1000:
                return 'Звездная энергия'
            elif lvl >= 500:
                return 'Атомная энергия'
            elif lvl >= 100:
                return 'Солнечная энергия'
            elif lvl >= 50:
                return 'Химикаты'
            elif lvl >= 10:
                return 'Железо'
            else:
                return 'Древесина'

        def create(self, name: str):
            con.ping(True)

            cur.execute("INSERT INTO Factory (owner_id, name) VALUES (%s, %s)", (self.player_id, name))
            con.commit()

        def delete(self):
            con.ping(True)

            cur.execute("DELETE FROM Factory WHERE owner_id = %s", (self.player_id,))
            con.commit()

        def exists(self) -> bool:
            con.ping(True)

            cur.execute("SELECT owner_id FROM Factory WHERE owner_id = %s", (self.player_id,))
            return not (cur.fetchone() is None)


