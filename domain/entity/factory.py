import math
import random
import time

from pydantic import BaseModel

from common.exceptions import DuringWorkException


class Product(BaseModel):
    name: str
    price_multiply: float
    time_to_create: float
    amount_multiply: float

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


class StorageProduct(BaseModel):
    product: Product
    storage: Storage
    amount: int


class AvailableProduct(BaseModel):
    product: Product
    factory: "Factory"


class Factory(BaseModel):
    id: int
    name: str
    storage: Storage = Storage()
    level: int = 10
    end_work_time: float = 0
    tax: int = 0
    workers: int = 10

    def __str__(self):
        return f"""\
🏭 *{self.name}*
🔧 *Уровень:* {self.level}
🚧 *Статус:* {"Работает" if self.state else "Не работает"}
💸 *Налоги:* {self.tax}
👷‍ *Работники:* {self.workers}
📦 *Товара на складе:* {self.storage.stock}
"""

    @property
    def minutes_to_work(self) -> float:
        return math.ceil(self.work_time_remaining / 60 * 10) / 10

    @property
    def upgrade_time(self) -> int:
        return (self.level + 5) * 5 + random.randint(1, 10)

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
    def max_workers(self) -> int:
        return self.level

    @property
    def available_workers(self) -> int:
        return self.level - self.workers

    @property
    def work_time_remained(self) -> float:
        return self.end_work_time - time.time()

    @property
    def state(self) -> bool:
        return self.work_time_remained > 0.0

    def start_workers(self, time_amount: float) -> float:
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

    def remove_tax(self) -> None:
        self.tax = 0
