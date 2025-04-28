import asyncio
from typing import Any

from common import settings
from common.exceptions import (
    AppException,
    NotEnoughPointsException,
    TaxException,
)

from ..entity import Factory, Product, StorageProduct, User
from ..entity.factory import StartFactoryEvent
from ..events import EventBus, on_event
from ..events.event_types import EventType
from ..interfaces import FactoryRepository
from .base import EventBased, SafeCall


class FactoryService:
    @staticmethod
    def hire_worker(factory: Factory) -> Factory:
        if factory.hire_available == 0:
            raise AppException("Максимальное количество рабочих достигнуто")
        factory.hire()
        return factory

    @staticmethod
    def start(factory: Factory, time: float) -> None:
        if factory.state:
            return
        if factory.workers == 0:
            raise AppException("Нельзя запустить фабрику без рабочих")
        if factory.tax > settings.TAX_LIMIT:
            raise TaxException
        factory.start_work(time)


class MoneyService:
    def __init__(self, event_bus: EventBus):
        self.event_bus = event_bus

    async def charge(self, user: User, amount: int) -> None:
        if not user.can_buy(amount):
            raise NotEnoughPointsException
        await self.event_bus.emit(
            EventType.SubtractMoney, data={"user": user, "amount": amount}
        )


class WorkSimulator:
    @staticmethod
    async def wait(time: float) -> None:
        await asyncio.sleep(time)


class UCFactory(SafeCall, EventBased):
    def __init__(self, repository: FactoryRepository, event_bus: EventBus):
        super().__init__(event_bus)
        self.repository = repository
        self.logic = FactoryService()
        self.money = MoneyService(event_bus)

    async def get_by_name(self, name: str) -> Factory | None:
        return await self.repository.by_name(name)

    async def start_factory(
        self, factory: Factory, time: float, product: Product
    ) -> Any:
        self.logic.start(factory, time)
        await self.repository.update(factory)

        await self.event_bus.emit(
            EventType.StartFactory,
            data=StartFactoryEvent(
                factory=factory,
                workers=factory.workers,
                time=time,
                product=product,
            ),
        )

    async def get_available_products(self, factory: Factory) -> list[Product]:
        return await self.repository.get_available_products(factory)

    async def find_product_by_name(
        self, factory: Factory, name: str
    ) -> Product | None:
        products = await self.get_available_products(factory)
        return next((p for p in products if p.name == name), None)

    @on_event(EventType.StartFactory)
    async def handle_start_factory(self, data: StartFactoryEvent) -> None:
        await WorkSimulator.wait(data.time)

        bonus = data.factory.get_bonus(data)
        await self.repository.update(data.factory)
        await self.insert_product_in_storage(
            StorageProduct(
                product=data.product,
                amount=bonus,
                storage=data.factory.storage,
            )
        )

        await self.event_bus.emit(
            EventType.EndFactoryWork,
            data={"factory": data.factory, "stock": bonus},
        )

    async def insert_product_in_storage(
        self, storage_product: StorageProduct
    ) -> None:
        await self.repository.add_product_in_storage(storage_product)
