from dishka import Provider, Scope, make_async_container

from domain import use_cases
from domain.events import EventBus
from domain.interfaces import (
    FactoryRepository,
    ShopRepository,
    UserMoneyRepository,
    UserRepository,
)
from domain.interfaces.factory import (
    FactoryTaxRepository,
    FactoryWorkersRepository,
)
from domain.interfaces.storage import StorageRepository
from domain.use_cases.base import DependencyRequired

from .events.eventbus import MemoryEventBus
from .repositories import (
    FactoryRepositoryImpl,
    ShopRepositoryImpl,
    UserRepositoryImpl,
)
from .repositories.factory import (
    FactoryTaxRepositoryImpl,
    FactoryWorkersRepositoryImpl,
)
from .repositories.storage import StorageRepositoryImpl
from .repositories.user_repository import UserMoneyRepositoryImpl
from .utils import get_children, load_packages

provider = Provider(scope=Scope.APP)
provider.provide(UserMoneyRepositoryImpl, provides=UserMoneyRepository)
provider.provide(UserRepositoryImpl, provides=UserRepository)


provider.provide(ShopRepositoryImpl, provides=ShopRepository)

provider.provide(FactoryRepositoryImpl, provides=FactoryRepository)
provider.provide(FactoryTaxRepositoryImpl, provides=FactoryTaxRepository)
provider.provide(
    FactoryWorkersRepositoryImpl, provides=FactoryWorkersRepository
)

provider.provide(StorageRepositoryImpl, provides=StorageRepository)


provider.provide(MemoryEventBus, provides=EventBus)

load_packages(use_cases)

for child in get_children(DependencyRequired):
    provider.provide(child)

container = make_async_container(provider)
