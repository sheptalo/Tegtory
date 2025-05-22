import dataclasses
from typing import Any

from domain.entities import User
from domain.events import EventType, on_event
from domain.interfaces import UserRepository
from domain.use_cases.base import EventBased


@dataclasses.dataclass(frozen=True)
class UserEvent(EventBased):
    repo: UserRepository

    @on_event(EventType.SubtractMoney)
    async def _subtract_user_money(self, data: dict[str, Any]) -> None:
        user = data.get("user")
        amount = data.get("amount")

        if not isinstance(user, User) or not isinstance(amount, int):
            return

        user.subtract_money(amount)
        await self.repo.update(user)
