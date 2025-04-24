from domain.entity import Factory, User
from domain.interfaces import UserRepository
from domain.use_cases.base import EventBased, SafeCall

from ..entity.factory import Product, StartFactoryEvent
from ..events import EventBus, EventType, on_event


class UCUser(SafeCall, EventBased):
    def __init__(self, repo: UserRepository, event_bus: EventBus) -> None:
        super().__init__(event_bus)
        self.repository = repo

    async def create(self, user: User) -> User:
        return await self.repository.create(user)

    async def create_if_not_exist(
        self, user_id: int, name: str, username: str
    ) -> None:
        user = await self.get(user_id)
        if not user:
            await self.create(User(id=user_id, name=name, username=username))

    async def start_work(
        self, factory: Factory, product: Product, time: float, user: User
    ) -> None:
        if user.state:
            return

        user.start_work(time)
        await self.repository.update(user)
        await self.event_bus.emit(
            EventType.StartFactory,
            data=StartFactoryEvent(
                factory=factory, time=time, product=product
            ),
        )

    @on_event(EventType.SubtractMoney)
    async def _subtract_user_money(self, user: User, amount: int) -> None:
        user.substract_money(amount)
        await self.repository.update(user)
