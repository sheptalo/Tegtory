from domain.entities import Factory, Storage
from domain.interfaces import FactoryRepository
from domain.interfaces.storage import StorageRepository
from domain.queries.factory import GetFactoryQuery, GetStorageQuery
from domain.use_cases.queries.base import BaseQueryHandler


class GetFactoryQueryHandler(BaseQueryHandler[GetFactoryQuery]):
    object_type = GetFactoryQuery

    def __init__(self, repo: FactoryRepository) -> None:
        self.repo = repo

    async def execute(self, query: GetFactoryQuery) -> Factory | None:
        return await self.repo.get(query.factory_id)


class GetStorageQueryHandler(BaseQueryHandler[GetStorageQuery]):
    object_type = GetStorageQuery

    def __init__(self, repo: StorageRepository) -> None:
        self.repo = repo

    async def execute(self, query: GetStorageQuery) -> Storage | None:
        return await self.repo.get(query.factory_id)
