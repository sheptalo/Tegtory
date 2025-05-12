from domain.entities import User
from domain.interfaces import UserRepository
from domain.queries.user import UserQuery
from domain.use_cases.queries.base import BaseQueryHandler


class GetUserQueryHandler(BaseQueryHandler[UserQuery]):
    object_type = UserQuery

    def __init__(self, repo: UserRepository) -> None:
        self.repo = repo

    async def handle(self, query: UserQuery) -> User | None:
        return await self.repo.get(query.user_id)
