from typing import Protocol

from domain.entity import Factory, Product, StorageProduct

from .base import CrudRepository


class FactoryRepository(CrudRepository[Factory]):
    async def by_name(self, name: str) -> Factory | None:
        pass

    async def upgrade(self, factory_id: int) -> Factory | None:
        pass

    async def add_available_product(self, factory: Factory, product: Product) -> tuple[Factory, Product]:
        pass

    async def get_available_products(self, factory: Factory) -> list[Product]:
        pass

    async def add_product_in_storage(self, storage_product: StorageProduct) -> StorageProduct:
        pass


class FactoryTaxRepository(Protocol):
    async def increase_tax(self, factory_id: int, amount: int) -> None:
        pass

    async def remove_tax(self, factory_id: int) -> None:
        pass


class FactoryWorkersRepository(Protocol):
    async def hire(self, factory_id: int) -> None:
        pass

    async def fire(self, factory_id: int) -> None:
        pass