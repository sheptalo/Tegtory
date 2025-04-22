from domain.interfaces import UserRepository
from domain.queries.user import UserQuery
from domain.use_cases.queries.base import BaseQueryHandler


class GetUserQueryHandler(BaseQueryHandler):
    object_type = UserQuery

    def __init__(self, repo: UserRepository):
        self.repo = repo

    async def __call__(self, query: UserQuery):
        return await self.repo.get(query.user_id)
