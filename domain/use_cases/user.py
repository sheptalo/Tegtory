from domain.entity import User
from domain.interfaces import IUserRepository
from domain.use_cases.base import BaseUseCase

from ..context.factory import StartWorkContext
from ..entity.factory import StartFactoryEvent
from ..events import EventType, IEventBus, on_event


class UCUser(BaseUseCase):
    def __init__(self, repo: IUserRepository, event_bus: IEventBus) -> None:
        super().__init__(event_bus)
        self.repository = repo

    async def create(self, user: User) -> User:
        return self.repository.create(user)

    async def update(self, user: User) -> User:
        return self.repository.update(user)

    async def get(self, user_id: int) -> User | None:
        return self.repository.get(user_id)

    async def create_if_not_exist(
        self, user_id: int, name: str, username: str
    ) -> None:
        user = await self.get(user_id)
        if not user:
            await self.create(User(id=user_id, name=name, username=username))

    async def start_work(self, ctx: StartWorkContext) -> None:
        user = ctx.user

        if user.state:
            return

        user.start_work(ctx.time)
        self.repository.update(user)
        await self.event_bus.emit(
            EventType.StartFactory,
            data=StartFactoryEvent(
                factory=ctx.factory,
                time=ctx.time,
                product=ctx.product,
            ),
        )

    @on_event(EventType.SubtractMoney)
    async def _subtract_user_money(self, user: User, amount: int) -> None:
        user.substract_money(amount)
        self.repository.update(user)
