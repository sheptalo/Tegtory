from ...entities import Shop
from ...interfaces import ShopRepository
from ...queries.shop import (
    ListShopDeliveryQuery,
    ListShopNoDeliveryQuery,
    ListShopQuery,
    ShopQuery,
)
from .base import BaseQueryHandler


class ListShopQueryHandler(BaseQueryHandler[ListShopQuery]):
    object_type = ListShopQuery

    def __init__(self, repo: ShopRepository):
        self.repo = repo

    async def handle(self, query: ListShopQuery) -> list[Shop]:
        return await self.repo.all()


class ShopQueryHandler(BaseQueryHandler[ShopQuery]):
    object_type = ShopQuery

    def __init__(self, repo: ShopRepository):
        self.repo = repo

    async def handle(self, query: ShopQuery) -> Shop | None:
        return await self.repo.by_name(query.title)


class ListShopNoDeliveryQueryHandler(
    BaseQueryHandler[ListShopNoDeliveryQuery]
):
    object_type = ListShopNoDeliveryQuery

    def __init__(self, repo: ShopRepository):
        self.repo = repo

    async def handle(self, query: ListShopNoDeliveryQuery) -> list[Shop]:
        return await self.repo.all_not_required_delivery()


class ListShopDeliveryQueryHandler(BaseQueryHandler[ListShopDeliveryQuery]):
    object_type = ListShopDeliveryQuery

    def __init__(self, repo: ShopRepository):
        self.repo = repo

    async def handle(self, query: ListShopDeliveryQuery) -> list[Shop]:
        return await self.repo.all_required_delivery()
