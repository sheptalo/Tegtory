from pydantic import BaseModel

from domain.entity.contract import BaseContract
from domain.entity.factory import Factory, Product
from domain.entity.shop import Shop
from domain.entity.user import User


class LogisticContract(BaseContract):
    product: Product
    amount: float
    destination: Shop
    price_km: float
    factory: Factory
    company: "LogisticCompany"


class Transport(BaseModel):
    name: str
    speed: float
    price: float
    max_size: float
    max_weight: float


class LogisticCompanyTransport(BaseModel):
    transport: Transport
    company: "LogisticCompany"
    amount: int = 1


class LogisticCompany(BaseModel):
    id: int
    title: str
    description: str
    owner: User | None = None
    is_bot: bool = True
