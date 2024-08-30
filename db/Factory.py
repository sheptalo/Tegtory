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
🏭 *{self.name.replace('_',' ')}*
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
        """
        cur.execute("SELECT owner_id FROM Factory WHERE owner_id = %s", (self.owner_id,))
        return not (cur.fetchone() is None)

    @property
    def type(self):
        """
        :return: type of factory
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
        """
        cur.execute("SELECT state FROM Factory WHERE owner_id = %s", (self.owner_id,))
        return cur.fetchone()[0]

    @state.setter
    def state(self, value):
        cur.execute("UPDATE Factory SET state = %s WHERE owner_id = %s", (value, self.owner_id))
        con.commit()

    @property
    def start_work_at(self) -> int:
        """
        :return: start work at
        """
        cur.execute("SELECT started_work_at FROM Factory WHERE owner_id = %s", (self.owner_id,))
        return cur.fetchone()[0]

    @start_work_at.setter
    def start_work_at(self, value):
        cur.execute("UPDATE Factory SET started_work_at = %s WHERE owner_id = %s", (value, self.owner_id))
        con.commit()

    @property
    def level(self) -> int:
        """
        :return: level of factory
        """
        cur.execute("SELECT lvl FROM Factory WHERE owner_id = %s", (self.owner_id,))
        return cur.fetchone()[0]

    @level.setter
    def level(self, value):
        cur.execute("UPDATE Factory SET lvl = %s WHERE owner_id=%s", (value, self.owner_id,))
        con.commit()

    @property
    def name(self) -> str:
        cur.execute("SELECT name FROM Factory WHERE owner_id = %s", (self.owner_id,))
        return cur.fetchone()[0]

    @name.setter
    def name(self, value):
        cur.execute("UPDATE Factory SET name = %s WHERE owner_id=%s", (value, self.owner_id,))
        con.commit()

    @property
    def workers(self):
        """
        :return: number of workers
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
        """
        cur.execute("SELECT tax FROM Factory WHERE owner_id = %s", (self.owner_id,))
        return cur.fetchone()[0]

    @tax.setter
    def tax(self, value):
        cur.execute("UPDATE Factory SET tax = %s WHERE owner_id=%s", (value, self.owner_id,))
        con.commit()

    @property
    def eco(self):
        """
        :return: eco amount of factory
        """
        cur.execute("SELECT ecology FROM Factory WHERE owner_id = %s", (self.owner_id,))
        return cur.fetchone()[0]

    @eco.setter
    def eco(self, value):
        cur.execute("UPDATE Factory SET ecology = %s WHERE owner_id=%s", (value, self.owner_id,))
        con.commit()

    @property
    def verification(self):
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
        """
        cur.execute("SELECT stock FROM Factory WHERE owner_id = %s", (self.owner_id,))
        return cur.fetchone()[0]

    @stock.setter
    def stock(self, value):
        cur.execute('UPDATE Factory SET stock = %s WHERE owner_id=%s', (value, self.owner_id,))
        con.commit()
