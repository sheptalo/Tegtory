import math
import time

from pydantic import BaseModel


class Dignity(BaseModel):
    name: str
    user: "User"


class User(BaseModel):
    id: int
    name: str
    username: str
    money: int = 5000000000
    stolar: int = 0
    rating: int = 0
    league: int = "Не в лиге"
    titles: list[str] = list([])
    is_admin: bool = False
    end_work_time: float = 0

    def __str__(self):
        return f"""\
🌟 *Паспорт {self.name}*

💲 *Баланс:* {self.money:,}
⚔️ *SC:* {self.stolar:,}

🏆 *Рейтинг:* {self.rating:,}
🛡️ *Лига:* {self.league}

№ {self.id * (len(self.username) ** 2) // 2}
"""

    @property
    def minutes_to_work(self) -> float:
        return math.ceil(self.work_time_remaining / 60 * 10) / 10

    @property
    def work_time_remaining(self):
        return self.end_work_time - time.time()

    @property
    def state(self):
        return self.work_time_remaining > 0.0

    def start_work(self, time_amount: float | int):
        if not self.state:
            self.end_work_time = time.time() + time_amount

    def set_name(self, name):
        self.name = name

    def substract_money(self, amount: int):
        self.money -= amount

    def can_buy(self, price: int):
        return self.money >= price
