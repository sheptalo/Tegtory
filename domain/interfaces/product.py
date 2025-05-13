from typing import Protocol

from domain.entities import Product


class ProductRepository(Protocol):
    async def by_name(self, name: str) -> Product | None:
        pass

    async def all(self) -> list[Product]:
        pass

    async def create(self, product: Product) -> None:
        pass

    async def update(self, product: Product) -> None:
        pass
