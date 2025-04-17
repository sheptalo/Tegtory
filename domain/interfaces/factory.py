from domain.entity import Factory, Product, Storage, StorageProduct

from .base import ICrudRepository


class IFactoryRepository(ICrudRepository[Factory]):
    def by_name(self, name: str) -> Factory | None:
        pass

    def get_storage(self, factory: Factory) -> Storage:
        pass

    def update_storage(self, storage: Storage) -> Storage:
        pass

    def create_storage(self, factory: Factory) -> Storage:
        pass

    def add_available_product(
        self, factory: Factory, product: Product
    ) -> tuple[Factory, Product]:
        pass

    def get_available_products(self, factory: Factory) -> list[Product]:
        pass

    def add_product_in_storage(
        self, storage_product: StorageProduct
    ) -> StorageProduct:
        pass
