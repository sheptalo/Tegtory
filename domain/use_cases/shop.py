from domain.entity import Shop, ShopContract, ShopProduct
from domain.events import IEventBus
from domain.interfaces.shop import IShopRepository
from domain.use_cases.base import BaseUseCase


class UCShop(BaseUseCase):
    def __init__(self, repo: IShopRepository, event_bus: IEventBus) -> None:
        super().__init__(event_bus)
        self.repository = repo

    async def all(self) -> list[Shop] | None:
        return self.repository.all()

    async def by_name(self, name) -> Shop | None:
        return self.repository.by_name(name)

    async def sign_contract(self, contract: ShopContract) -> ShopContract:
        return self.repository.sign_contract(contract)

    async def get_product_list(
        self, shop: Shop, is_demand: bool = False
    ) -> list[ShopProduct]:
        return self.repository.get_products(shop, is_demand)

    async def send_resources(self):
        pass

    async def specific_shop_product_by_id(
        self, product_id: int
    ) -> ShopProduct:
        return self.repository.get_product_by_id(product_id)
