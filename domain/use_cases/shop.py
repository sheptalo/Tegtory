from domain.entity import Shop, ShopContract, ShopProduct
from domain.events import EventBus
from domain.interfaces.shop import ShopRepository
from domain.use_cases.base import EventBased, SafeCall


class UCShop(SafeCall, EventBased):
    def __init__(self, repo: ShopRepository, event_bus: EventBus) -> None:
        super().__init__(event_bus)
        self.repository = repo

    async def all(self) -> list[Shop] | None:
        return await self.repository.all()

    async def by_name(self, name) -> Shop | None:
        return await self.repository.by_name(name)

    async def sign_contract(self, contract: ShopContract) -> ShopContract:
        return await self.repository.sign_contract(contract)

    async def demand_product_list(self, shop: Shop) -> list[ShopProduct]:
        return await self.repository.get_products(shop, True)

    async def send_resources(self):
        pass

    async def shop_product_by_id(self, product_id: int) -> ShopProduct:
        return await self.repository.get_product_by_id(product_id)

    async def preview_contract(
        self, factory, shop_product: ShopProduct
    ) -> ShopContract:
        price_per_one = ShopContract.calculate_price_per_one(shop_product)
        contract = ShopContract(
            factory=factory,
            shop=shop_product.shop,
            price_per_one=price_per_one,
            product=shop_product.product,
            amount=shop_product.amount,
            delivery_required=shop_product.shop.delivery_required,
        )
        return contract
