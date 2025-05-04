from common.exceptions import NotEnoughPointsException
from domain.entities import User
from domain.events import EventType
from domain.use_cases.base import EventBased


class MoneyService(EventBased):
    async def charge(self, user: User, amount: int) -> None:
        if not user.can_buy(amount):
            raise NotEnoughPointsException
        await self.event_bus.emit(
            EventType.SubtractMoney, data={"user": user, "amount": amount}
        )
