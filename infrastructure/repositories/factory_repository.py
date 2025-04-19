import logging

from domain.entity import Factory, Product, Storage, StorageProduct
from domain.interfaces import IFactoryRepository

logger = logging.getLogger(__name__)


class FactoryRepository(IFactoryRepository):
    def __init__(self):
        self.factories = []
        self.storages = {}
        self.available_products = {}

    async def get(self, owner_id: int) -> Factory:
        return await self._filter_factories(owner_id)

    async def create(self, factory: Factory) -> Factory:
        logger.info(f"Creating Factory {factory.name} by user {factory.id}")
        self.factories.append(factory)
        return factory

    async def update(self, user: Factory) -> Factory:
        pass

    async def by_name(self, name: str) -> Factory | None:
        for i in filter(lambda f: f.name == name, self.factories):
            return i
        return None

    async def get_storage(self, factory: Factory) -> Storage:
        return self.storages.get(factory.id)

    async def create_storage(self, factory: Factory) -> Storage:
        storage = Storage()
        self.storages[factory.id] = storage
        return storage

    async def add_available_product(
        self, factory: Factory, product: Product
    ) -> tuple[Factory, Product]:
        if not self.available_products.get(factory.id):
            self.available_products[factory.id] = []
        self.available_products[factory.id].append(product)
        return factory, product

    async def get_available_products(self, factory: Factory) -> list[Product]:
        return self.available_products.get(factory.id, [])

    async def _filter_factories(self, user_id: int) -> Factory | None:
        for i in filter(lambda u: u.id == user_id, self.factories):
            return i
        return None

    async def add_product_in_storage(
        self, storage_product: StorageProduct
    ) -> StorageProduct:
        storage = storage_product.storage
        if not storage.products.get(storage_product.product):
            storage.products[storage_product.product] = 0
        storage.products[storage_product.product] += storage_product.amount

        return storage_product
