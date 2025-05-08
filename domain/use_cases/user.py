from typing import Any

from domain.interfaces import EventBus, UserRepository
from domain.use_cases.base import EventBased

from ..entities import User
from ..events import EventType, on_event


class UserEvent(EventBased):
    def __init__(self, repo: UserRepository, event_bus: EventBus) -> None:
        super().__init__(event_bus)
        self.repository = repo

    @on_event(EventType.SubtractMoney)
    async def _subtract_user_money(self, data: dict[str, Any]) -> None:
        user = data.get("user")
        amount = data.get("amount")

        if not isinstance(user, User) or not isinstance(amount, int):
            return

        user.subtract_money(amount)
        await self.repository.update(user)
