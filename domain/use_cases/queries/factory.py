from domain.interfaces import FactoryRepository
from domain.interfaces.storage import StorageRepository
from domain.queries.factory import GetFactoryQuery, GetStorageQuery
from domain.use_cases.queries.base import BaseQueryHandler


class GetFactoryQueryHandler(BaseQueryHandler):
    object_type = GetFactoryQuery

    def __init__(self, repo: FactoryRepository):
        self.repo = repo

    async def __call__(self, query: GetFactoryQuery):
        return await self.repo.get(query.factory_id)


class GetStorageQueryHandler(BaseQueryHandler):
    object_type = GetStorageQuery

    def __init__(self, repo: StorageRepository):
        self.repo = repo

    async def __call__(self, query: GetStorageQuery):
        return await self.repo.get(query.factory_id)
