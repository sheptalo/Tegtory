from ...entities import Shop
from ...interfaces import ShopRepository
from ...queries.shop import ListShopQuery
from .base import BaseQueryHandler


class ListShopQueryHandler(BaseQueryHandler[ListShopQuery]):
    object_type = ListShopQuery

    def __init__(self, repo: ShopRepository):
        self.repo = repo

    async def handle(self, query: ListShopQuery) -> list[Shop]:
        return await self.repo.all()
