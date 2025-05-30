import dataclasses

from domain.entities import Factory, Product, User


@dataclasses.dataclass(kw_only=True, frozen=True)
class StartWorkContext:
    factory: Factory
    product: Product
    time: float
    user: User | None = None


@dataclasses.dataclass(kw_only=True, frozen=True)
class UserFactoryContext:
    user: User
    factory: Factory
