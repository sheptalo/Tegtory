from domain.entities import Product
from domain.interfaces.base import CrudRepository


class ProductRepository(CrudRepository[Product]):
    async def by_name(self, name: str) -> Product | None:
        pass
