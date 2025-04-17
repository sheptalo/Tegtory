from domain.entity import Factory, Product, User
from domain.interfaces import IUserRepository
from domain.use_cases.base import BaseUseCase

from ..events import EventType, IEventBus, on_event


class UCUser(BaseUseCase):
    def __init__(self, repo: IUserRepository, event_bus: IEventBus) -> None:
        self.repository = repo
        super().__init__(event_bus)

    async def create(self, user: User) -> User:
        return self.repository.create(user.id, user.name, user.username)

    async def update(self, user: User) -> User:
        return self.repository.update(user)

    async def get(self, user_id: int) -> User | None:
        return self.repository.get(user_id)

    async def create_if_not_exist(
        self, user_id: int, name: str, username: str
    ) -> None:
        user = self.repository.get(user_id)
        if not user:
            self.repository.create(user_id, name, username)

    async def start_work(
        self, user: User, factory: Factory, product: Product, time: float
    ) -> User:
        if user.state:
            return user
        user.work_to(time)
        await self.event_bus.emit(
            EventType.StartFactory,
            factory=factory,
            time=time,
            product=product,
        )
        self.repository.update(user)
        return user

    @on_event(EventType.SubtractMoney)
    async def _subtract_user_money_event(
        self, user: User, amount: int
    ) -> None:
        user.money -= amount
        self.repository.update(user)
