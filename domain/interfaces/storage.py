from typing import Protocol


class StorageRepository(Protocol):
    async def get(self, factory_id: int):
        pass

    async def upgrade(self, factory_id: int):
        pass

    async def create(self, factory_id: int):
        pass

    async def insert_product_in_storage(
        self, factory_id: int, product_id: int, amount: int
    ):
        pass
