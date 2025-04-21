from dishka import Provider, Scope, make_async_container

from domain.events import IEventBus
from domain.interfaces import (
    FactoryRepository,
    ShopRepository,
    UserMoneyRepository,
    UserRepository,
)
from domain.interfaces.factory import FactoryTaxRepository
from domain.use_cases import UCFactory, UCShop, UCUser
from domain.use_cases.commands.factory import CreateFactoryHandler, PayFactoryTaxHandler, UpgradeStorageHandler

from .events.eventbus import MemoryEventBus
from .repositories import (
    FactoryRepositoryImpl,
    ShopRepositoryImpl,
    UserRepositoryImpl,
)
from .repositories.factory import FactoryTaxRepositoryImpl
from .repositories.user_repository import UserMoneyRepositoryImpl

provider = Provider(scope=Scope.APP)
provider.provide(UserMoneyRepositoryImpl, provides=UserMoneyRepository)
provider.provide(UserRepositoryImpl, provides=UserRepository)

provider.provide(ShopRepositoryImpl, provides=ShopRepository)
provider.provide(FactoryRepositoryImpl, provides=FactoryRepository)
provider.provide(FactoryTaxRepositoryImpl, provides=FactoryTaxRepository)

provider.provide(MemoryEventBus, provides=IEventBus)

provider.provide(UCUser)
provider.provide(UCFactory)
provider.provide(UCShop)

provider.provide(CreateFactoryHandler)
provider.provide(PayFactoryTaxHandler)
provider.provide(UpgradeStorageHandler)

container = make_async_container(provider)
