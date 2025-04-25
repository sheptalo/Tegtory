from domain.entity import Storage
from domain.interfaces.storage import StorageRepository

_storages: dict[int, Storage] = {}


class StorageRepositoryImpl(StorageRepository):
    async def create(self, factory_id: int) -> Storage:
        _storages[factory_id] = Storage()
        return _storages[factory_id]

    async def upgrade(self, factory_id: int) -> None:
        _storages[factory_id].upgrade()

    async def get(self, factory_id: int) -> Storage | None:
        return _storages.get(factory_id)
