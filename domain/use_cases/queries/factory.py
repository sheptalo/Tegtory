from domain.interfaces import FactoryRepository
from domain.queries.factory import GetFactoryQuery
from domain.use_cases.queries.base import BaseQueryHandler


class GetFactoryQueryHandler(BaseQueryHandler):
    object_type = GetFactoryQuery

    def __init__(self, repo: FactoryRepository):
        self.repo = repo

    async def __call__(self, query: GetFactoryQuery):
        return await self.repo.get(query.factory_id)
