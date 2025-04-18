import asyncio

from common import settings
from common.exceptions import (
    AppException,
    NotEnoughPointsException,
    TaxException,
)
from common.settings import TAX_LIMIT

from ..context.factory import StartWorkContext, UserFactoryContext
from ..entity import Factory, Product, Storage, StorageProduct, User
from ..entity.factory import StartFactoryEvent
from ..events import IEventBus, on_event
from ..events.event_types import EventType
from ..interfaces import IFactoryRepository
from .base import BaseUseCase


class UCFactory(BaseUseCase):
    def __init__(self, repository: IFactoryRepository, event_bus: IEventBus):
        super().__init__(event_bus)
        self.repository = repository

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
        if await self.get(factory.id) or await self.by_name(factory.name):
            return factory

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

    async def pay_tax(self, ctx: UserFactoryContext) -> Factory:
        tax = ctx.factory.tax
        if not ctx.user.can_buy(tax):
            raise NotEnoughPointsException
        if tax == 0:
            return ctx.factory

        factory = ctx.factory
        factory.remove_tax()
        self.repository.update(factory)
        await self.event_bus.emit(
            EventType.SubtractMoney, user=ctx.user, amount=tax
        )
        return factory

    async def upgrade(self, ctx: UserFactoryContext) -> Factory:
        factory = ctx.factory
        if not ctx.user.can_buy(factory.upgrade_price):
            raise NotEnoughPointsException

        upgrade_price = factory.upgrade_price
        factory.upgrade()
        self.repository.update(factory)

        await self.event_bus.emit(
            EventType.SubtractMoney,
            user=ctx.user,
            amount=upgrade_price,
        )
        return factory

    async def upgrade_storage(self, storage: Storage, user: User) -> Storage:
        if not user.can_buy(storage.upgrade_price):
            raise NotEnoughPointsException
        price = storage.upgrade_price
        storage.upgrade()
        self.repository.update_storage(storage)

        await self.event_bus.emit(
            EventType.SubtractMoney, amount=price, user=user
        )
        return storage

    async def hire(
        self,
        ctx: UserFactoryContext,
    ) -> Factory:
        factory = ctx.factory

        if not ctx.user.can_buy(factory.upgrade_price):
            raise NotEnoughPointsException
        elif factory.hire_available == 0:
            raise AppException("Максимальное количество рабочих достигнуто")

        price = factory.hire_price
        factory.hire()
        self.repository.update(factory)
        await self.event_bus.emit(
            EventType.SubtractMoney, user=ctx.user, amount=price
        )
        return factory

    async def start_factory(self, ctx: StartWorkContext) -> None:
        factory = ctx.factory

        if factory.state:
            return
        if factory.workers == 0:
            raise AppException(
                "Нельзя запустить фабрику в которой нет рабочих"
            )
        if factory.tax > TAX_LIMIT:
            raise TaxException

        factory.start_work(ctx.time)
        self.repository.update(factory)

        data = StartFactoryEvent(
            factory=factory,
            workers=factory.workers,
            time=ctx.time,
            product=ctx.product,
        )
        await self.event_bus.emit(EventType.StartFactory, data=data)

    async def get_available_products(self, factory: Factory) -> list[Product]:
        return self.repository.get_available_products(factory)

    async def get_available_product_by_name(
        self, factory: Factory, product_name: str
    ) -> Product | None:
        products = self.repository.get_available_products(factory)
        for product in filter(lambda p: p.name == product_name, products):
            return product

    @on_event(EventType.StartFactory)
    async def start_factory_event(self, data: StartFactoryEvent) -> None:
        await self._emulate_work(data.time)

        bonus = data.factory.get_bonus(data)
        self.repository.update(data.factory)

        await self.insert_product_in_storage(data, bonus)
        await self.event_bus.emit(
            EventType.EndFactoryWork, factory=data.factory, stock=bonus
        )

    @staticmethod
    async def _emulate_work(time: float) -> None:
        await asyncio.sleep(time)

    async def insert_product_in_storage(
        self, data: StartFactoryEvent, amount: int
    ) -> None:
        self.repository.add_product_in_storage(
            StorageProduct(
                product=data.product,
                amount=amount,
                storage=data.factory.storage,
            )
        )
