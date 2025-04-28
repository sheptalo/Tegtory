from domain.commands.user import RegisterUserCommand
from domain.entity import User
from domain.interfaces import UserRepository
from domain.use_cases.commands.base import BaseCommandHandler


class RegisterUserCommandHandler(BaseCommandHandler):
    object_type = RegisterUserCommand

    def __init__(self, repo: UserRepository) -> None:
        self.repo = repo

    async def __call__(self, query: RegisterUserCommand) -> User | None:
        return await self.repo.create(
            User(id=query.user_id, name=query.name, username=query.username)
        )
