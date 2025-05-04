from typing import Any

from domain.entities import Factory, User
from domain.interfaces import EventBus, UserRepository
from domain.use_cases.base import EventBased, SafeCall

from ..entities.factory import Product, StartFactoryEvent
from ..events import EventType, on_event


class UCUser(SafeCall, EventBased):
    def __init__(self, repo: UserRepository, event_bus: EventBus) -> None:
        super().__init__(event_bus)
        self.repository = repo

    async def start_work(
        self, factory: Factory, product: Product, time: float, user: User
    ) -> None:
        user.start_work(time)
        await self.repository.update(user)
        await self.event_bus.emit(
            EventType.StartFactory,
            data=StartFactoryEvent(
                factory=factory, time=time, product=product
            ),
        )


class UserEvent(EventBased):
    def __init__(self, repo: UserRepository, event_bus: EventBus) -> None:
        super().__init__(event_bus)
        self.repository = repo

    @on_event(EventType.SubtractMoney)
    async def _subtract_user_money(self, data: dict[str, Any]) -> None:
        user = data.get("user")
        amount = data.get("amount")

        if not user or not amount:
            return

        user.substract_money(amount)
        await self.repository.update(user)
