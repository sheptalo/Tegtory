from dishka import Provider, Scope, make_async_container

from domain.events import IEventBus
from domain.interfaces import (
    IFactoryRepository,
    IShopRepository,
    IUserRepository,
)
from domain.use_cases import UCFactory, UCShop, UCUser

from .events.eventbus import MemoryEventBus
from .repositories import FactoryRepository, ShopRepository, UserRepository

provider = Provider(scope=Scope.APP)
provider.provide(UserRepository, provides=IUserRepository)
provider.provide(ShopRepository, provides=IShopRepository)
provider.provide(
    FactoryRepository, provides=IFactoryRepository
)

provider.provide(MemoryEventBus, provides=IEventBus)

provider.provide(UCUser)
provider.provide(UCFactory)
provider.provide(UCShop)

container = make_async_container(provider)
