from domain.entities import Shop, ShopProduct
from domain.interfaces import EventBus
from domain.interfaces.shop import ShopRepository
from domain.use_cases.base import EventBased, SafeCall


class UCShop(SafeCall, EventBased):
    def __init__(self, repo: ShopRepository, event_bus: EventBus) -> None:
        super().__init__(event_bus)
        self.repository = repo

    async def all(self) -> list[Shop]:
        return await self.repository.all()

    async def by_name(self, name: str) -> Shop | None:
        return await self.repository.by_name(name)

    async def shop_product_by_id(self, product_id: int) -> ShopProduct | None:
        return await self.repository.get_product_by_id(product_id)
