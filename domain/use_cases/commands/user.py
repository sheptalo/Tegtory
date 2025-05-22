import dataclasses

from domain.commands.user import RegisterUserCommand, StartUserWorkCommand
from domain.entities import User
from domain.entities.factory import StartFactoryEvent
from domain.events import EventType
from domain.interfaces import EventBus, UserRepository
from domain.use_cases.commands.base import BaseCommandHandler


@dataclasses.dataclass(frozen=True)
class RegisterUserCommandHandler(BaseCommandHandler):
    object_type = RegisterUserCommand

    repo: UserRepository

    async def execute(self, cmd: RegisterUserCommand) -> User | None:
        return await self.repo.create(
            User(id=cmd.user_id, name=cmd.name, username=cmd.username)
        )


@dataclasses.dataclass(frozen=True)
class StartUserWorkCommandHandler(BaseCommandHandler):
    object_type = StartUserWorkCommand

    repo: UserRepository
    event_bus: EventBus

    async def execute(self, cmd: StartUserWorkCommand) -> None:
        cmd.user.start_work(cmd.time)
        await self.repo.update(cmd.user)
        await self.event_bus.emit(
            EventType.StartFactory,
            data=StartFactoryEvent(
                factory=cmd.factory, time=cmd.time, product=cmd.product
            ),
        )
