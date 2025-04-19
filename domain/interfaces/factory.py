from domain.entity import Factory, Product, Storage, StorageProduct

from .base import ICrudRepository


class IFactoryRepository(ICrudRepository[Factory]):
    async def by_name(self, name: str) -> Factory | None:
        pass

    async def get_storage(self, factory: Factory) -> Storage:
        pass

    async def update_storage(self, storage: Storage) -> Storage:
        pass

    async def create_storage(self, factory: Factory) -> Storage:
        pass

    async def add_available_product(
        self, factory: Factory, product: Product
    ) -> tuple[Factory, Product]:
        pass

    async def get_available_products(self, factory: Factory) -> list[Product]:
        pass

    async def add_product_in_storage(
        self, storage_product: StorageProduct
    ) -> StorageProduct:
        pass
