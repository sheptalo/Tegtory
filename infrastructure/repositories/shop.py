from domain.entities import Shop, ShopProduct
from domain.interfaces.shop import ShopRepository


class ShopRepositoryImpl(ShopRepository):
    def __init__(self) -> None:
        self.shops: list[Shop] = []
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

    async def delete(self, item_id: int) -> None:
        pass

    async def by_name(self, name: str) -> Shop | None:
        for i in filter(lambda shop: shop.title == name, self.shops):
            return i
        return None

    async def get_products(
        self, shop: Shop, is_demand: bool = False
    ) -> list[ShopProduct]:
        res = []
        for i in filter(
            lambda x: x.is_demand == is_demand and x.shop.id == shop.id,
            self.shop_products,
        ):
            res.append(i)
        return res

    async def add_product(self, product: ShopProduct) -> ShopProduct:
        self.shop_products.append(product)
        product.id = len(self.shop_products)
        return product

    async def get_product_by_id(self, product_id: int) -> ShopProduct | None:
        for i in filter(
            lambda shop: shop.id == product_id, self.shop_products
        ):
            return i
        return None
