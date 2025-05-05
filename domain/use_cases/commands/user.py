from domain.commands.user import RegisterUserCommand, StartUserWorkCommand
from domain.entities import User
from domain.entities.factory import StartFactoryEvent
from domain.events import EventType
from domain.interfaces import EventBus, UserRepository
from domain.use_cases.base import EventBased
from domain.use_cases.commands.base import BaseCommandHandler


class RegisterUserCommandHandler(BaseCommandHandler):
    object_type = RegisterUserCommand

    def __init__(self, repo: UserRepository) -> None:
        self.repo = repo

    async def execute(self, cmd: RegisterUserCommand) -> User | None:
        return await self.repo.create(
            User(id=cmd.user_id, name=cmd.name, username=cmd.username)
        )


class StartUserWorkCommandHandler(BaseCommandHandler, EventBased):
    object_type = StartUserWorkCommand

    def __init__(self, repo: UserRepository, event_bus: EventBus) -> None:
        super().__init__(event_bus)
        self.repo = repo

    async def execute(self, cmd: StartUserWorkCommand) -> None:
        cmd.user.start_work(cmd.time)
        await self.repo.update(cmd.user)
        await self.event_bus.emit(
            EventType.StartFactory,
            data=StartFactoryEvent(
                factory=cmd.factory, time=cmd.time, product=cmd.product
            ),
        )
