from typing import Protocol

from domain.entities import Shop, ShopContract, ShopProduct


class ShopRepository(Protocol):
    async def all(self) -> list[Shop]:
        pass

    async def get(self, item_id: int) -> Shop | None:
        pass

    async def create(self, item: Shop) -> Shop:
        pass

    async def update(self, item: Shop) -> Shop:
        pass

    async def by_name(self, name: str) -> Shop | None:
        pass

    async def sign_contract(self, contract: ShopContract) -> ShopContract:
        pass

    async def update_contract(self, contract: ShopContract) -> ShopContract:
        pass

    async def add_product(self, product: ShopProduct) -> ShopProduct:
        pass

    async def get_products(self, shop: Shop) -> list[ShopProduct]:
        pass

    async def get_product_by_id(self, product_id: int) -> ShopProduct | None:
        pass
