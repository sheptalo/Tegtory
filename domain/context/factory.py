from pydantic import BaseModel

from domain.entities import Factory, Product, User


class StartWorkContext(BaseModel):
    factory: Factory
    product: Product
    time: float
    user: User | None = None


class UserFactoryContext(BaseModel):
    user: User
    factory: Factory
