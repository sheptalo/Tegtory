from domain.entity import Shop, ShopContract, ShopProduct

from .base import ICrudRepository


class IShopRepository(ICrudRepository[Shop]):
    def by_name(self, name):
        pass

    def sign_contract(self, contract: ShopContract) -> ShopContract:
        pass

    def update_contract(self, contract: ShopContract) -> ShopContract:
        pass

    def add_product(self, product: ShopProduct) -> ShopProduct:
        pass

    def get_products(
        self, shop: Shop, is_demand: bool = False
    ) -> list[ShopProduct]:
        pass

    def get_product_by_id(self, product_id: int) -> ShopProduct | None:
        pass
