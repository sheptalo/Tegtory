from domain.entity import Storage
from domain.interfaces.storage import StorageRepository

_storages: dict[int, Storage] = {}


class StorageRepositoryImpl(StorageRepository):
    async def create(self, factory_id: int):
        _storages[factory_id] = Storage()
        return await self.get(factory_id)

    async def upgrade(self, factory_id: int):
        _storages[factory_id].upgrade()

    async def get(self, factory_id: int):
        return _storages.get(factory_id)
