from bot import con, cur


class Player:
    """
    :type user_id: int | str
    A class to represent a player
    connects to player database
    """
    def __init__(self, user_id):
        try:
            self.user_id = int(user_id)
        except:
            cur.execute("SELECT telegram_id FROM Users WHERE username = %s", (user_id.replace('@', ''), ))
            self.user_id = cur.fetchone()[0]

    def __str__(self):
        _clan = '0'
        _clan = '0'
        if _clan == '0':
            _clan = 'Не в обьединении'
        _text = f"""
🌟*{self.nickname}*🌟

💲 *Баланс:* {self.money:,}
⚔️ *Столар:* {self.stolar:,}

🏆 *Рейтинг:* {self.rating}
🛡️ *Лига:* {self.league}

🌎 *Oбъединение:* {self.clan.name.replace('_', ' ')}

*Идентификатор*: {self.iternal_id}
"""
        title = self.titles
        if title:
            _text += f'\n\n🏆 *Титулы:* \n'
            for name in title.split():
                _text += f"- {name.replace('_', ' ')}\n"
        return _text

    async def create(self, username: str, user: str):
        """
        creates a new player and adds it to the database
        """
        cur.execute("INSERT INTO"
                    " Users(telegram_id, name, league, username) VALUES (%s, %s, '', %s)", (self.user_id, username, user))
        con.commit()

    @property
    def iternal_id(self) -> int:
        """
        returns the iternal id of player in database
        """
        cur.execute("SELECT id FROM Users WHERE telegram_id = %s", (self.user_id,))
        return cur.fetchone()[0]

    @property
    def exist(self) -> bool:
        """
        checks if the player exists
        """
        cur.execute("SELECT telegram_id FROM Users WHERE telegram_id = %s", (self.user_id,))
        return not (cur.fetchone() is None)

    @property
    def nickname(self) -> str:
        """
        returns the nickname of player
        :return: nickname
        """
        cur.execute("SELECT name FROM Users WHERE telegram_id=%s", (self.user_id,))
        return cur.fetchone()[0]

    @nickname.setter
    def nickname(self, value: str):
        cur.execute("UPDATE Users SET name=%s WHERE telegram_id=%s", (self.user_id, value))
        con.commit()

    @property
    def username(self):
        cur.execute("SELECT username FROM Users WHERE telegram_id=%s", (self.user_id,))
        return cur.fetchone()[0]

    @username.setter
    def username(self, value):
        cur.execute("UPDATE Users SET username=%s WHERE telegram_id=%s", (value, self.user_id, ))
        con.commit()

    @property
    def titles(self) -> str:
        cur.execute("SELECT Titles FROM Users WHERE telegram_id=%s", (self.user_id,))
        return cur.fetchone()[0]

    @titles.setter
    def titles(self, value):
        cur.execute("UPDATE Users SET Titles=%s WHERE telegram_id=%s", (value, self.user_id))
        con.commit()

    @property
    def money(self):
        cur.execute(f'SELECT money FROM Users WHERE telegram_id = {self.user_id}')
        return cur.fetchone()[0]

    @money.setter
    def money(self, value: int):
        cur.execute(f'UPDATE Users SET money = {value} WHERE telegram_id = {self.user_id}')
        con.commit()

    @property
    def stolar(self):
        cur.execute(f'SELECT stolar FROM Users WHERE telegram_id = {self.user_id}')
        return cur.fetchone()[0]

    @stolar.setter
    def stolar(self, value: int):
        cur.execute(f"UPDATE Users SET stolar = {value} WHERE telegram_id = {self.user_id}")
        con.commit()

    @property
    def league(self):
        cur.execute(f'SELECT league FROM Users WHERE telegram_id = {self.user_id}')
        return cur.fetchone()[0]

    @league.setter
    def league(self, value):
        cur.execute(f"UPDATE Users SET league = %s WHERE telegram_id = {self.user_id}", (value,))
        con.commit()

    @property
    def rating(self):
        cur.execute(f'SELECT rating FROM Users WHERE telegram_id = {self.user_id}')
        return cur.fetchone()[0]

    @rating.setter
    def rating(self, value):
        cur.execute(f"UPDATE Users SET rating = {value} WHERE telegram_id = {self.user_id}")
        con.commit()

    @property
    def farm(self) -> int:
        cur.execute(f'SELECT farm_click FROM Users WHERE telegram_id = {self.user_id}')
        return cur.fetchone()[0]

    @farm.setter
    def farm(self, value: int):
        cur.execute(f'UPDATE Users SET farm_click = {value} WHERE telegram_id = {self.user_id}')
        con.commit()

    @property
    def is_working(self) -> int:
        cur.execute(f'SELECT isWorking FROM Users WHERE telegram_id = {self.user_id}')
        return bool(cur.fetchone()[0])

    @is_working.setter
    def is_working(self, value: int):
        cur.execute(f'UPDATE Users SET isWorking = {value} WHERE telegram_id = {self.user_id}')
        con.commit()

    @property
    def tickets(self) -> str:
        cur.execute(f'SELECT tickets FROM Users WHERE telegram_id = {self.user_id}')
        return cur.fetchone()[0]

    @tickets.setter
    def tickets(self, value: str):
        cur.execute(f'UPDATE Users SET tickets = %s WHERE telegram_id = {self.user_id}', (value,))
        con.commit()

    @property
    def work_at(self) -> int:
        cur.execute(f'SELECT WorkedAt FROM Users WHERE telegram_id = {self.user_id}')
        return cur.fetchone()[0]

    @work_at.setter
    def work_at(self, value: int):
        cur.execute(f'UPDATE Users SET workedAt = {value} WHERE telegram_id = {self.user_id}')
        con.commit()

    @property
    def clan(self):
        return self.__Clan(self)

    class __Clan:
        def __init__(self, player):
            self.player = player

        @staticmethod
        def can_create(name: str) -> bool:
            cur.execute("SELECT clan_leader FROM Users WHERE clan_name=%s AND clan_leader = 1", (name,))
            return cur.fetchone() is None

        @staticmethod
        def exists(name) -> bool:
            cur.execute(f'SELECT clan_name FROM Users WHERE clan_name=%s', (name,))
            return cur.fetchone() is not None

        @property
        def name(self) -> str:
            cur.execute(f'SELECT clan_name FROM Users WHERE telegram_id = {self.player.user_id}')
            return cur.fetchone()[0]

        @name.setter
        def name(self, value: str):
            cur.execute(f'UPDATE Users SET clan_name = %s WHERE telegram_id = {self.player.user_id}', (value,))
            con.commit()

        @property
        def leader(self) -> int:
            cur.execute(f'SELECT clan_leader FROM Users WHERE telegram_id = {self.player.user_id}')
            return cur.fetchone()[0]

        @leader.setter
        def leader(self, value: int):
            cur.execute(f'UPDATE Users SET clan_leader = {value} WHERE telegram_id = {self.player.user_id}')

    @property
    def ref(self) -> str:
        cur.execute('SELECT ref FROM Users WHERE telegram_id = %s', (self.user_id,))
        return cur.fetchone()[0]

    @ref.setter
    def ref(self, value: str):
        cur.execute(f'UPDATE Users SET ref = {value} WHERE telegram_id = {self.user_id}')
        con.commit()
