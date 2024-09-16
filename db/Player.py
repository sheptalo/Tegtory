from bot import con, cur


class Player:
    """
    :type user_id: int | str
    A class to represent a player
    connects to player database
    >>> Player(6646169400).exist
    True
    >>> Player('@sinortax').exist
    True
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

        >>> Player(123456789).iternal_id
        5
        """
        cur.execute("SELECT id FROM Users WHERE telegram_id = %s", (self.user_id,))
        return cur.fetchone()[0]

    @property
    def exist(self) -> bool:
        """
        checks if the player exists
        >>> Player(0).exist
        False
        >>> Player(123456789).exist
        True
        """
        cur.execute("SELECT telegram_id FROM Users WHERE telegram_id = %s", (self.user_id,))
        return not (cur.fetchone() is None)

    @property
    def nickname(self) -> str:
        """
        returns the nickname of player
        :return: nickname
        >>> Player(123456789).nickname
        '5'
        """
        cur.execute("SELECT name FROM Users WHERE telegram_id=%s", (self.user_id,))
        return cur.fetchone()[0]

    @nickname.setter
    def nickname(self, value: str):
        """

        >>> player = Player(123456789)
        >>> old_value = player.nickname
        >>> player.nickname = 'nick'
        >>> player.nickname
        'nick'
        >>> player.nickname = 'user'
        >>> player.nickname
        'user'
        >>> player.nickname = old_value
        """
        cur.execute("UPDATE Users SET name=%s WHERE telegram_id=%s", (self.user_id, value))
        con.commit()

    @property
    def username(self):
        """
        >>> Player(123456789).username
        'use'
        """
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
        """
        returns the money of the player


        >>> Player(123456789).money
        500
        """
        cur.execute(f'SELECT money FROM Users WHERE telegram_id = {self.user_id}')
        return cur.fetchone()[0]

    @money.setter
    def money(self, value: int):
        """
        sets the money of the player
        :param value: int

        >>> player = Player(123456789)
        >>> old_value = player.money
        >>> player.money = 123
        >>> player.money
        123
        >>> player.money = 500
        >>> player.money
        500
        >>> player.money = old_value
        """
        cur.execute(f'UPDATE Users SET money = {value} WHERE telegram_id = {self.user_id}')
        con.commit()

    @property
    def stolar(self):
        cur.execute(f'SELECT stolar FROM Users WHERE telegram_id = {self.user_id}')
        return cur.fetchone()[0]

    @stolar.setter
    def stolar(self, value: int):
        """
        sets the stolar of the player

        >>> player = Player(123456789)
        >>> old_value = player.stolar
        >>> player.stolar = 123
        >>> player.stolar
        123
        >>> player.stolar = 500
        >>> player.stolar
        500
        >>> player.stolar = old_value
        """
        cur.execute(f"UPDATE Users SET stolar = {value} WHERE telegram_id = {self.user_id}")
        con.commit()

    @property
    def league(self):
        """

        >>> Player(123456789).league
        'Не в лиге'
        """
        cur.execute(f'SELECT league FROM Users WHERE telegram_id = {self.user_id}')
        return cur.fetchone()[0]

    @league.setter
    def league(self, value):
        cur.execute(f"UPDATE Users SET league = %s WHERE telegram_id = {self.user_id}", (value,))
        con.commit()

    @property
    def rating(self):
        """
        >>> Player(123456789).rating
        0
        """
        cur.execute(f'SELECT rating FROM Users WHERE telegram_id = {self.user_id}')
        return cur.fetchone()[0]

    @rating.setter
    def rating(self, value):
        """
        sets the rating of the player

        >>> player = Player(123456789)
        >>> old_value = player.rating
        >>> player.rating = 1
        >>> player.rating
        1
        >>> player.rating = old_value
        """
        cur.execute(f"UPDATE Users SET rating = {value} WHERE telegram_id = {self.user_id}")
        con.commit()

    @property
    def farm(self) -> int:
        """
        player last farm time


        >>> Player(123456789).farm
        0
        """
        cur.execute(f'SELECT farm_click FROM Users WHERE telegram_id = {self.user_id}')
        return cur.fetchone()[0]

    @farm.setter
    def farm(self, value: int):
        """
        sets the farm_click value of the player

        >>> player = Player(123456789)
        >>> old_value = player.farm
        >>> player.farm = 1230
        >>> player.farm
        '1230'
        >>> player.farm = 5000
        >>> player.farm
        '5000'
        >>> player.farm = old_value
        """
        cur.execute(f'UPDATE Users SET farm_click = {value} WHERE telegram_id = {self.user_id}')
        con.commit()

    @property
    def is_working(self) -> int:
        cur.execute(f'SELECT isWorking FROM Users WHERE telegram_id = {self.user_id}')
        return bool(cur.fetchone()[0])

    @is_working.setter
    def is_working(self, value: int):
        """
        sets the is_working value of the player

        >>> player = Player(123456789)
        >>> old_value = player.is_working
        >>> player.is_working = 1
        >>> player.is_working
        '1'
        >>> player.is_working = 0
        >>> player.is_working
        '0'
        >>> player.is_working = old_value
        """
        cur.execute(f'UPDATE Users SET isWorking = {value} WHERE telegram_id = {self.user_id}')
        con.commit()

    @property
    def tickets(self) -> str:
        cur.execute(f'SELECT tickets FROM Users WHERE telegram_id = {self.user_id}')
        return cur.fetchone()[0]

    @tickets.setter
    def tickets(self, value: str):
        """
        sets the tickets of the player

        >>> player = Player(123456789)
        >>> old_value = player.tickets
        >>> player.tickets = '1230 0321'
        >>> player.tickets
        '1230 0321'
        >>> player.tickets = '5000 2345 876'
        >>> player.tickets
        '5000 2345 876'
        >>> player.tickets = old_value
        """
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
        """
        returns the clan class


        >>> player = Player(123456789)
        >>> clan = player.clan
        >>> clan.name
        ''
        >>> clan.leader
        0
        >>> clan.name = '1'
        >>> clan.name
        '1'
        >>> clan.name = ''
        """
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
        """
        returns the ref

        >>> Player(123456789).ref
        ''
        >>> Player(6646169400).ref
        '6646169400'
        """
        cur.execute('SELECT ref FROM Users WHERE telegram_id = %s', (self.user_id,))
        return cur.fetchone()[0]

    @ref.setter
    def ref(self, value: str):
        """
        sets the ref of the player


        >>> player = Player(123456789)
        >>> old_value = player.ref
        >>> player.ref = 1230
        >>> player.ref
        '1230'
        >>> player.ref = 5000
        >>> player.ref
        '5000'
        >>> player.ref = old_value
        """
        cur.execute(f'UPDATE Users SET ref = {value} WHERE telegram_id = {self.user_id}')
        con.commit()
