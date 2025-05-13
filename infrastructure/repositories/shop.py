from domain.entities import Shop, ShopProduct
from domain.interfaces.shop import ShopRepository


class ShopRepositoryImpl(ShopRepository):
    def __init__(self) -> None:
        self.shops: list[Shop] = [
            Shop(id=1, title="dd", description="dsd", distance=1)
        ]
        self.shop_products: list[ShopProduct] = []

    async def all(self) -> list[Shop]:
        return self.shops

    async def get(self, item_id: int) -> Shop | None:
        for i in filter(lambda shop: shop.id == item_id, self.shops):
            return i
        return None

    async def create(self, item: Shop) -> Shop:
        self.shops.append(item)
        item.id = len(self.shops)
        return item

    async def update(self, item: Shop) -> Shop:
        return item

    async def by_name(self, name: str) -> Shop | None:
        for i in filter(lambda shop: shop.title == name, self.shops):
            return i
        return None
