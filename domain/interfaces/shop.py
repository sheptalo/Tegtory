import abc

from domain.entity import Shop, ShopContract, ShopProduct

from .base import CrudRepository


class ShopRepository(CrudRepository[Shop], abc.ABC):
    @abc.abstractmethod
    async def by_name(self, name: str) -> Shop | None:
        pass

    @abc.abstractmethod
    async def sign_contract(self, contract: ShopContract) -> ShopContract:
        pass

    @abc.abstractmethod
    async def update_contract(self, contract: ShopContract) -> ShopContract:
        pass

    @abc.abstractmethod
    async def add_product(self, product: ShopProduct) -> ShopProduct:
        pass

    @abc.abstractmethod
    async def get_products(
        self, shop: Shop, is_demand: bool = False
    ) -> list[ShopProduct]:
        pass

    @abc.abstractmethod
    async def get_product_by_id(self, product_id: int) -> ShopProduct | None:
        pass
