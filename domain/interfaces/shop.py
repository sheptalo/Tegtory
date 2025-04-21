from domain.entity import Shop, ShopContract, ShopProduct

from .base import CrudRepository


class ShopRepository(CrudRepository[Shop]):
    async def by_name(self, name):
        pass

    async def sign_contract(self, contract: ShopContract) -> ShopContract:
        pass

    async def update_contract(self, contract: ShopContract) -> ShopContract:
        pass

    async def add_product(self, product: ShopProduct) -> ShopProduct:
        pass

    async def get_products(
        self, shop: Shop, is_demand: bool = False
    ) -> list[ShopProduct]:
        pass

    async def get_product_by_id(self, product_id: int) -> ShopProduct | None:
        pass
