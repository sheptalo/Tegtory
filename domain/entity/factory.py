import math
import random
import time

from pydantic import BaseModel

from common.exceptions import DuringWorkException


class Product(BaseModel):
    name: str
    price_multiply: float = 1
    time_to_create: int = 10
    amount_multiply: float = 1

    def __hash__(self):
        return hash(self.name)


class Storage(BaseModel):
    max_stock: int = 20
    products: dict[Product, int] = dict()

    @property
    def stock(self):
        return sum(self.products.values())

    @property
    def upgrade_price(self) -> int:
        return self.max_stock // 2 + 78

    def upgrade(self):
        self.max_stock += 10

    def is_can_insert(self, product_amount: int) -> bool:
        return self.stock + product_amount <= self.max_stock

    def get_available_amount(self) -> int:
        return self.max_stock - self.stock

    def adjust_bonus(self, bonus):
        if not self.is_can_insert(bonus):
            bonus = self.get_available_amount()
        return bonus


class StorageProduct(BaseModel):
    product: Product
    storage: Storage
    amount: int


class AvailableProduct(BaseModel):
    product: Product
    factory: "Factory"


class StartFactoryEvent(BaseModel):
    factory: "Factory"
    time: float | int
    product: Product
    workers: int = 1


class WorkersFactory(BaseModel):
    id: int
    workers: int = 10
    level: int = 10

    @property
    def hire_price(self) -> int:
        return (1 + self.workers) * 300

    @property
    def hire_available(self) -> int:
        return self.level - self.workers


class Factory(BaseModel):
    id: int
    name: str
    storage: Storage = Storage()
    level: int = 10
    end_work_time: float = 0
    tax: int = 1
    workers: int = 10

    def __str__(self):
        return f"""\
🏭 *{self.name}*
🔧 *Уровень:* {self.level}
🚧 *Статус:* {"Работает" if self.state else "Не работает"}
💸 *Налоги:* {self.tax}
👷‍ *Работники:* {self.workers}
"""

    @property
    def minutes_to_work(self) -> float:
        return math.ceil(self.work_time_remained / 60 * 10) / 10

    @property
    def hire_price(self) -> int:
        return (1 + self.workers) * 300

    @property
    def hire_available(self) -> int:
        return self.level - self.workers

    @property
    def upgrade_price(self) -> int:
        return (self.level + 2) * 370

    @property
    def work_time_remained(self) -> float:
        return self.end_work_time - time.time()

    @property
    def state(self) -> bool:
        return self.work_time_remained > 0.0

    def start_work(self, time_amount: float) -> float:
        if not self.state:
            self.end_work_time = time.time() + time_amount
        return self.end_work_time

    def rename(self, name) -> None:
        self.name = name

    def upgrade(self) -> None:
        if self.state:
            raise DuringWorkException

        self.level += 1

    def hire(self) -> None:
        if self.state:
            raise DuringWorkException
        self.workers += 1

    def set_tax(self, amount: int) -> None:
        self.tax = random.randint(1, 5) * amount // 3

    def get_bonus(self, data: StartFactoryEvent) -> int:
        bonus = self.calculate_bonus(data)
        bonus = self.storage.adjust_bonus(bonus)
        self.set_tax(bonus)
        return bonus

    @staticmethod
    def calculate_bonus(data: StartFactoryEvent) -> int:
        return data.time // data.product.time_to_create * data.workers
