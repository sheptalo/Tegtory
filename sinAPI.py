from requests import get, post, put, delete as delet
from dotenv import load_dotenv
from os import environ

load_dotenv()
api_url = environ.get('API_URL') + '/api/v1/'


class Base:
    params = eval(get(api_url + 'params').text)

    def __init__(self, user_id, vk, api_key):
        self.headers = {"Authorization": f"Bearer {api_key}"}
        self.player_id = str(user_id)
        self.get_url = f"{api_url}{self.__class__.__name__}/{user_id}/"
        self.post_url = f"{api_url}{self.__class__.__name__}"
        self.vk = vk

    def __getitem__(self, name):
        return self.__get(name)

    def __getattr__(self, name):
        return self.__get(name)

    def __setattr__(self, name, value):
        self.__setitem__(name, value)

    def __setitem__(self, name, value):
        self.__set(name, value)

    def set(self, values: dict):
        put(self.post_url, json=values, headers=self.headers)

    def get(self, values: str):
        return eval(get(self.get_url + values, headers=self.headers).text)

    def __set(self, name, value):
        if self.params is None and name in eval(get(api_url + 'params').text) or name in self.params:
            if self.vk:
                put(self.post_url, headers=self.headers, json={'vk_id': self.player_id, name: value})
            elif self.__class__.__name__ == 'Player':
                put(self.post_url, headers=self.headers, json={'telegram_id': self.player_id, name: value})
            else:
                put(self.post_url, headers=self.headers, json={'owner_id': str(self.player_id), name: value})
        self.__dict__[name] = value

    def __get(self, name):
        if self.params is None and name in eval(get(api_url + 'params').text) or name in self.params:
            return eval(get(self.get_url + name, headers=self.headers).text)[0]
        elif name in self.__dict__:
            return self.__dict__[name]


class SinApi:
    def __init__(self, api_key):
        self.api_key = api_key
        self.headers = {"Authorization": f"Bearer {self.api_key}"}

    def player(self, user_id):
        """
        player = api.player(id)
        player = api.player(vk_id)
        player.global_change({
        'telegram_id': self.player_id,
        'vk_id': self.player_id,
        'значение для изменения', значение,
        'значение для изменения', значение,
        ...
        })
        """
        return self.Player(user_id, self.api_key)

    def factory(self, owner_id):
        """
        factory = api.factory(id пользователя)

        получаем значения из бд
        factory.name или factory.get('name')
        получаем список значений factory.get('name,workers') -> [name, workers]

        изменяем данные
        factory.name = ''
        или
        factory.global_change({
        'owner_id': id пользователя,
        'значение для изменения', значение,
        'значение для изменения', значение,
        ...
    })
        """
        return self.Factory(owner_id, self.api_key)

    def find_factory(self, name):
        req = get(f'{api_url}findFactory/{name}',
                  headers=self.headers).text
        return self.factory(req) if req != '0' else req

    def stock(self):
        return eval(get(f'{api_url}stock',
                        headers=self.headers).text)[0]

    def league_update(self):
        post(f'{api_url}leagueUpdate', headers=self.headers,
             allow_redirects=True)

    def lottery_start(self):
        return eval(get(f'{api_url}startLottery', headers=self.headers).text)

    def reset_tickets(self):
        post(f'{api_url}resetTickets', headers=self.headers)

    class Player(Base):
        def __init__(self, user_id, api_key):
            vk = str(user_id).startswith('vk_')
            try:
                if not vk:
                    int(user_id)
            except:
                user_id = get(f'{api_url}findUser/{user_id.replace('@', '')}',
                              headers={"Authorization": f"Bearer {api_key}"}).text
            super().__init__(user_id, vk, api_key)

        def __str__(self):
            user_data = self.get('name,money,stolar,rating,league,clan_name,id,titles')
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
            post(self.post_url, headers=self.headers,
                 json={"telegram_id": self.player_id, 'username': username, 'user': user})

        @property
        def exist(self) -> bool:
            try:
                if self.telegram_id == int(self.player_id) or self.vk_id == int(self.player_id.replace('vk_', '')):
                    return True
            except:
                pass
            return False

        @property
        def is_banned(self) -> bool:
            return False

    class Factory(Base):
        def __init__(self, user_id, api_key):
            vk = str(user_id).startswith('vk_')
            super().__init__(user_id, vk, api_key)

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

        @property
        def exist(self) -> bool:
            try:
                req = get(self.get_url + 'owner_id', headers=self.headers)
                if req.status_code != 404:
                    return True
            except:
                pass
            return False

        def create(self, name: str):
            post(self.post_url, headers=self.headers, json={'owner_id': self.player_id, 'name': name})

        def delete(self):
            delet(self.post_url, headers=self.headers, params={'owner_id': self.owner_id})

        def exists(self) -> bool:
            return self.exist
