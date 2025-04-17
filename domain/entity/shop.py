from datetime import datetime

from aiogram.types import User
from pydantic import BaseModel

from domain.entity.contract import BaseContract
from domain.entity.factory import Factory, Product


class Shop(BaseModel):
    id: int
    title: str
    description: str
    distance: int
    is_bot: bool = True
    owner: User | None = None

    @property
    def delivery_required(self):
        return self.distance > 10


class ShopProduct(BaseModel):
    id: int
    shop: Shop
    product: Product
    amount: int
    is_demand: bool = False
    created_at: datetime = datetime.now()


class ShopContract(BaseContract):
    shop: Shop
    factory: Factory
    product: Product
    amount: int
    price_per_one: int
    delivery_required: bool = False
