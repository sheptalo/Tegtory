from bot import cur, con
from db.Player import Player


class Factory:
    """
    :type owner_id: int | str
    Connects with user factory
    Recommend to use self.exists() to check if factory exists
    """
    @staticmethod
    def find(name):
        """
        :type name: str
        use this to find factory using name
        :param name:
        :return: factory
        >>> type(Factory.find(0))
        <class 'db.Factory.Factory'>
        """
        cur.execute(f'SELECT owner_id from Factory where name = %s', (name,))
        res = cur.fetchone()
        return Factory(res[0], True)

    def __init__(self, owner_id, skip=False):
        if owner_id > 0 and not skip:
            self.owner_id = Player(owner_id).iternal_id
        elif owner_id < 0:
            self.owner_id = owner_id
        if skip:
            self.owner_id = owner_id

    def __str__(self):
        return f"""
🏭 *{self.name.replace('_', ' ')}*
🔧 *Уровень:* {self.level}
⚙️ *Тип:* {self.type}
🚧 *Статус:* {'Работает' if self.state == 1 else 'Не работает'}
💸 *Налоги:* {self.tax}
👷‍ *Работники:* {self.workers}
♻️ *Вклад в экологию:* {self.eco}
📦 *Товара на складе:* {self.stock}
{'🔎 _Знак качества_' if self.verification == 1 else ''}
        """

    def __getitem__(self, item):
        """
        :param item:
        :return:
        >>> factory = Factory(1405684214)
        >>> factory['owner']
        1

        """
        return getattr(self, item)

    def create(self, name: str):
        """
        :type name: str
        creates a new factory
        :param name: name of new factory
        :return: None
        """
        cur.execute("INSERT INTO Factory (owner_id, name) VALUES (%s, %s)", (self.owner_id, name))
        con.commit()

    def delete(self):
        """
        deletes a factory
        :return: None
        """
        cur.execute("DELETE FROM Factory WHERE owner_id = %s", (self.owner_id,))
        con.commit()

    @property
    def owner(self) -> int:
        return self.owner_id

    def exists(self) -> bool:
        """
        checks if factory exists

        >>> Factory(1405684214).exists()
        True
        >>> Factory(0, True).exists()
        False
        """
        cur.execute("SELECT owner_id FROM Factory WHERE owner_id = %s", (self.owner_id,))
        return not (cur.fetchone() is None)

    @property
    def type(self):
        """
        :return: type of factory

        >>> Factory(10, True).type
        'Звездная энергия'
        """
        lvl = self.level

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
    def state(self):
        """
        :return: state of factory

        >>> Factory(10, True).state
        0
        """
        cur.execute("SELECT state FROM Factory WHERE owner_id = %s", (self.owner_id,))
        return cur.fetchone()[0]

    @state.setter
    def state(self, value):
        """
        sets state of factory

        :type value: int
        >>> factory = Factory(10, True)
        >>> factory.state = 1
        >>> factory.state
        1
        >>> factory.state = 0
        """
        cur.execute("UPDATE Factory SET state = %s WHERE owner_id = %s", (value, self.owner_id))
        con.commit()

    @property
    def start_work_at(self) -> int:
        """
        :return: start work at

        >>> Factory(10, True).start_work_at
        0
        """
        cur.execute("SELECT started_work_at FROM Factory WHERE owner_id = %s", (self.owner_id,))
        return cur.fetchone()[0]

    @start_work_at.setter
    def start_work_at(self, value):
        """

        :param value:
        :return:
        >>> factory = Factory(10, True)
        >>> factory.start_work_at = 10
        >>> factory.start_work_at
        10
        >>> factory.start_work_at = 0
        """
        cur.execute("UPDATE Factory SET started_work_at = %s WHERE owner_id = %s", (value, self.owner_id))
        con.commit()

    @property
    def level(self) -> int:
        """
        :return: level of factory

        >>> Factory(10, True).level
        1000
        """
        cur.execute("SELECT lvl FROM Factory WHERE owner_id = %s", (self.owner_id,))
        return cur.fetchone()[0]

    @level.setter
    def level(self, value):
        """

        :param value:
        :return: factory lvl


        >>> factory = Factory(10, True)
        >>> factory.level = 10
        10
        >>> factory.level = 1000
        """
        cur.execute("UPDATE Factory SET lvl = %s WHERE owner_id=%s", (value, self.owner_id,))
        con.commit()

    @property
    def name(self) -> str:
        """
        :return: name of factory

        >>> Factory(10, True).name
        'Мегалодон'
        """
        cur.execute("SELECT name FROM Factory WHERE owner_id = %s", (self.owner_id,))
        return cur.fetchone()[0]

    @name.setter
    def name(self, value):
        """

        >>> factory = Factory(10, True)
        >>> factory.name = 'test'
        >>> factory.name
        'test'
        >>> factory.name = 'Мегалодон'
        """
        cur.execute("UPDATE Factory SET name = %s WHERE owner_id=%s", (value, self.owner_id,))
        con.commit()

    @property
    def workers(self):
        """
        :return: number of workers

        >>> factory = Factory(10, True)
        >>> old_value = factory.workers
        >>> factory.workers = 1230
        >>> factory.workers
        1230
        >>> factory.workers = 5000
        >>> factory.workers
        5000
        >>> factory.workers = old_value
        """
        cur.execute("SELECT workers FROM Factory WHERE owner_id = %s", (self.owner_id,))
        return cur.fetchone()[0]

    @workers.setter
    def workers(self, value):
        cur.execute("UPDATE Factory SET workers = %s WHERE owner_id=%s", (value, self.owner_id,))
        con.commit()

    @property
    def tax(self) -> int:
        """
        :return: taxes of factory

        >>> Factory(10, True).tax
        234
        """
        cur.execute("SELECT tax FROM Factory WHERE owner_id = %s", (self.owner_id,))
        return cur.fetchone()[0]

    @tax.setter
    def tax(self, value):
        """

        >>> factory = Factory(10, True)
        >>> old_value = factory.tax
        >>> factory.tax = 1230
        >>> factory.tax
        '1230'
        >>> factory.tax = 5000
        >>> factory.tax
        '5000'
        >>> factory.tax = old_value
        """
        cur.execute("UPDATE Factory SET tax = %s WHERE owner_id=%s", (value, self.owner_id,))
        con.commit()

    @property
    def eco(self):
        """
        :return: eco amount of factory


        >>> factory = Factory(10, True)
        >>> old_value = factory.eco
        >>> factory.eco = 1230
        >>> factory.eco
        1230
        >>> factory.eco = 5000
        >>> factory.eco
        5000
        >>> factory.eco = old_value
        """
        cur.execute("SELECT ecology FROM Factory WHERE owner_id = %s", (self.owner_id,))
        return cur.fetchone()[0]

    @eco.setter
    def eco(self, value):
        cur.execute("UPDATE Factory SET ecology = %s WHERE owner_id=%s", (value, self.owner_id,))
        con.commit()

    @property
    def verification(self):
        """
        :return: verification of factory

        >>> factory = Factory(10, True)
        >>> old_value = factory.verification
        >>> factory.verification = 1
        >>> factory.verification
        1
        >>> factory.verification = 0
        >>> factory.verification
        0
        >>> factory.verification = old_value
        """
        cur.execute("SELECT verification FROM Factory WHERE owner_id = %s", (self.owner_id,))
        return cur.fetchone()[0]

    @verification.setter
    def verification(self, value):
        cur.execute('UPDATE Factory SET verification = %s WHERE owner_id=%s', (value, self.owner_id,))
        con.commit()

    @property
    def stock(self) -> int:
        """
        check stock amount from factory
        :return: stock amount

        >>> factory = Factory(10, True)
        >>> old_value = factory.stock
        >>> factory.stock = 1230
        >>> factory.stock
        1230
        >>> factory.stock = 5000
        >>> factory.stock
        5000
        >>> factory.stock = old_value
        """
        cur.execute("SELECT stock FROM Factory WHERE owner_id = %s", (self.owner_id,))
        return cur.fetchone()[0]

    @stock.setter
    def stock(self, value):
        cur.execute('UPDATE Factory SET stock = %s WHERE owner_id=%s', (value, self.owner_id,))
        con.commit()
