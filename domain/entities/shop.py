from datetime import datetime

from pydantic import BaseModel

from common.settings import DELIVERY_MIN_DISTANTION
from domain.entities.contract import BaseContract
from domain.entities.factory import Factory, Product


class Shop(BaseModel):
    id: int
    title: str
    description: str
    distance: int
    is_bot: bool = True

    @property
    def delivery_required(self) -> bool:
        return self.distance > DELIVERY_MIN_DISTANTION


class ShopProduct(BaseModel):
    id: int = 0
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
