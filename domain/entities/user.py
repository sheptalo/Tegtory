import math
import time

from pydantic import BaseModel

from common.exceptions import DuringWorkException


class Dignity(BaseModel):
    name: str
    user: "User"


class User(BaseModel):
    id: int
    name: str
    username: str
    money: int = 500
    stolar: int = 0
    rating: int = 0
    league: str = "Не в лиге"
    titles: list[str] = list([])
    is_admin: bool = False
    end_work_time: float = 0

    @property
    def minutes_to_work(self) -> float:
        return float(math.ceil(self.work_time_remaining / 60 * 10) / 10)

    @property
    def work_time_remaining(self) -> float:
        return self.end_work_time - time.time()

    @property
    def state(self) -> bool:
        return self.work_time_remaining > 0.0

    def start_work(self, time_amount: float | int) -> None:
        if self.state:
            raise DuringWorkException
        self.end_work_time = time.time() + time_amount

    def set_name(self, name: str) -> None:
        self.name = name

    def substract_money(self, amount: int) -> None:
        self.money -= amount

    def can_buy(self, price: int) -> bool:
        return self.money >= price
