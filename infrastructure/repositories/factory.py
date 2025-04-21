import logging

from domain.entity import Factory, Product, Storage, StorageProduct
from domain.interfaces import FactoryRepository
from domain.interfaces.factory import FactoryTaxRepository

logger = logging.getLogger(__name__)
_factories = []


def _filter_factories(user_id: int) -> Factory | None:
    for i in filter(lambda u: u.id == user_id, _factories):
        return i
    return None


class FactoryRepositoryImpl(FactoryRepository):
    def __init__(self):
        self.storages = {}
        self.available_products = {}

    async def get(self, owner_id: int) -> Factory:
        return _filter_factories(owner_id)

    async def create(self, factory: Factory) -> Factory:
        logger.info(f"Creating Factory {factory.name} by user {factory.id}")
        _factories.append(factory)
        return factory

    async def update(self, user: Factory) -> Factory:
        pass

    async def by_name(self, name: str) -> Factory | None:
        for i in filter(lambda f: f.name == name, _factories):
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

    async def add_product_in_storage(
        self, storage_product: StorageProduct
    ) -> StorageProduct:
        storage = storage_product.storage
        if not storage.products.get(storage_product.product):
            storage.products[storage_product.product] = 0
        storage.products[storage_product.product] += storage_product.amount

        return storage_product


class FactoryTaxRepositoryImpl(FactoryTaxRepository):
    def increase_tax(self, factory_id: int, amount: int) -> None:
        factory = _filter_factories(factory_id)
        factory.tax += amount

    def remove_tax(self, factory_id: int) -> None:
        factory = _filter_factories(factory_id)
        factory.tax = 0
