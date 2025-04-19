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

    def calculate_price_per_one(self, shop_product: ShopProduct):
        pass

    def __str__(self):
        return f"""
Контракт купли-продажи {self.created_at}

Фабрика {self.factory.name} именуемая в дальнейшем "Продавец", \
магазин {self.shop.title} именуемый в дальнейшем "Покупатель" \
в отношении {self.product.title} в дальнейшем "Товар"
заключили контракт о нижеследующем:

-----1. Предмет Договора-----

1.1 Продавец передает во владение покупателя, \
товар в количестве {self.amount} ед. по цене {self.price_per_one} за ед.

1.2 Товар подлежит использованию по его предназначению \
или дальнейшей оптовой (розничной) торговли

1.3 Доставка товара на покупателю будет осуществлена \
{"Продавцом" if self.delivery_required else "Покупателем"} \

-----2. Цена и порядок расчетов-----
2.1 Общая стоимость Товара составляет {self.amount * self.price_per_one} руб.
2.2 Оплата производится в течении 4 часов с момента \
подписания Акта приёмки-передачи Товара

-----3. Сроки поставки-----

3.1 Товар должен быть поставлен до {self.estimated_date}

-----4. Гарантии и Штрафы-----

4.1 в случае отсутсвия товара на складе покупателя после срока поставки \
контракт расторгается в одностороннем порядке

-----5. Реквизиты и подписи-----
Продавец: {self.factory.name}, Идентификатор {self.factory.id}
Покупатель: {self.shop.title}, Идентификатор {self.shop.id}
"""
