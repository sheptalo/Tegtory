from dishka import Provider, Scope, make_async_container

from domain.events import IEventBus
from domain.interfaces import (
    FactoryRepository,
    ShopRepository,
    UserMoneyRepository,
    UserRepository,
)
from domain.interfaces.factory import FactoryTaxRepository, FactoryWorkersRepository
from domain.interfaces.storage import StorageRepository
from domain.use_cases import UCFactory, UCShop, UCUser
from domain.use_cases.commands.factory import (
    CreateFactoryHandler,
    PayFactoryTaxHandler,
    UpgradeStorageHandler,
    UpgradeFactoryHandler, HireWorkerCommandHandler,
)
from domain.use_cases.queries.factory import GetFactoryQueryHandler
from domain.use_cases.queries.user import GetUserQueryHandler

from .events.eventbus import MemoryEventBus
from .repositories import (
    FactoryRepositoryImpl,
    ShopRepositoryImpl,
    UserRepositoryImpl,
)
from .repositories.factory import FactoryTaxRepositoryImpl, FactoryWorkersRepositoryImpl
from .repositories.storage import StorageRepositoryImpl
from .repositories.user_repository import UserMoneyRepositoryImpl

provider = Provider(scope=Scope.APP)
provider.provide(UserMoneyRepositoryImpl, provides=UserMoneyRepository)
provider.provide(UserRepositoryImpl, provides=UserRepository)


provider.provide(ShopRepositoryImpl, provides=ShopRepository)

provider.provide(FactoryRepositoryImpl, provides=FactoryRepository)
provider.provide(FactoryTaxRepositoryImpl, provides=FactoryTaxRepository)
provider.provide(FactoryWorkersRepositoryImpl, provides=FactoryWorkersRepository)

provider.provide(StorageRepositoryImpl, provides=StorageRepository)


provider.provide(MemoryEventBus, provides=IEventBus)


provider.provide(UCUser)
provider.provide(UCFactory)
provider.provide(UCShop)


provider.provide(GetFactoryQueryHandler)
provider.provide(GetUserQueryHandler)


provider.provide(CreateFactoryHandler)
provider.provide(PayFactoryTaxHandler)
provider.provide(UpgradeStorageHandler)
provider.provide(UpgradeFactoryHandler)
provider.provide(HireWorkerCommandHandler)

container = make_async_container(provider)
