import asyncio
import random

from common import settings
from common.exceptions import (
    AppException,
    NotEnoughPointsException,
    TaxException,
)
from common.settings import TAX_LIMIT

from ..entity import Factory, Product, Storage, StorageProduct, User
from ..events import IEventBus, on_event
from ..events.event_types import EventType
from ..interfaces import IFactoryRepository
from .base import BaseUseCase


class UCFactory(BaseUseCase):
    def __init__(self, repository: IFactoryRepository, event_bus: IEventBus):
        self.repository = repository
        super().__init__(event_bus)

    async def get_storage(self, factory) -> Storage | None:
        return self.repository.get_storage(factory)

    async def get(self, owner_id: int) -> Factory | None:
        factory = self.repository.get(owner_id)
        if factory:
            factory.storage = await self.get_storage(factory)
        return factory

    async def by_name(self, name: str) -> Factory | None:
        return self.repository.by_name(name)

    async def create(self, factory: Factory) -> Factory | None:
        if await self.get(factory.id):
            return factory
        elif await self.by_name(factory.name):
            return None
        factory = self.repository.create(factory)
        factory.storage = self.repository.create_storage(factory)
        for product in settings.DEFAULT_AVAILABLE_PRODUCTS:
            self.repository.add_available_product(factory, product)
        return factory

    async def rename(self, factory: Factory) -> Factory | None:
        existing_factory = await self.by_name(factory.name)
        if existing_factory and existing_factory.id != factory.id:
            return None
        return self.repository.update(factory)

    async def pay_tax(self, factory: Factory, user: User) -> Factory:
        tax = factory.tax
        if tax > user.money:
            raise NotEnoughPointsException
        if tax == 0:
            return factory
        factory.remove_tax()
        self.repository.update(factory)
        await self.event_bus.emit(
            EventType.SubtractMoney, user=user, amount=tax
        )
        return factory

    async def upgrade(self, factory: Factory, user: User) -> Factory:
        if factory.upgrade_price > user.money:
            raise NotEnoughPointsException
        upgrade_price = factory.upgrade_price
        factory.upgrade()
        await self.event_bus.emit(
            EventType.SubtractMoney,
            user=user,
            amount=upgrade_price,
        )
        self.repository.update(factory)
        return factory

    async def upgrade_storage(self, storage: Storage, user: User):
        if storage.upgrade_price > user.money:
            raise NotEnoughPointsException
        price = storage.upgrade_price
        storage.upgrade()

        await self.event_bus.emit(
            EventType.SubtractMoney, amount=price, user=user
        )

    async def hire(self, factory: Factory, user: User) -> Factory:
        if factory.hire_price > user.money:
            raise NotEnoughPointsException
        elif factory.hire_available == 0:
            raise AppException("Максимальное количество рабочих достигнуто")

        price = factory.hire_price
        factory.hire()
        self.repository.update(factory)
        await self.event_bus.emit(
            EventType.SubtractMoney, user=user, amount=price
        )
        return factory

    async def start_factory(
        self, factory: Factory, product: Product, time: float
    ) -> Factory:
        if factory.state:
            return factory
        if factory.workers == 0:
            raise AppException(
                "Нельзя запустить фабрику в которой нет рабочих"
            )
        if factory.tax > TAX_LIMIT:
            raise TaxException
        factory.start_workers(time)
        self.repository.update(factory)
        await self.event_bus.emit(
            EventType.StartFactory,
            factory=factory,
            time=time,
            product=product,
            workers=factory.workers,
        )
        return factory

    async def get_available_products(self, factory: Factory) -> list[Product]:
        return self.repository.get_available_products(factory)

    async def get_available_product_by_name(
        self, factory: Factory, product_name: str
    ) -> Product | None:
        products = self.repository.get_available_products(factory)
        for product in filter(lambda p: p.name == product_name, products):
            return product

    @on_event(EventType.StartFactory)
    async def start_factory_event(
        self,
        factory: Factory,
        time: float | int,
        product: Product,
        workers: int = 1,
    ) -> None:
        await asyncio.sleep(time)
        bonus = time // product.time_to_create * workers
        if factory.storage.stock + bonus > factory.storage.max_stock:
            bonus = factory.storage.max_stock - factory.storage.stock
        self.repository.add_product_in_storage(
            StorageProduct(
                product=product, amount=bonus, storage=factory.storage
            )
        )
        factory.tax += random.randint(1, 5) * bonus // 3
        self.repository.update(factory)
        await self.event_bus.emit(
            EventType.EndFactoryWork, factory=factory, stock=bonus
        )
