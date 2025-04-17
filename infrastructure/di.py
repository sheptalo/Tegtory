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

provider = Provider()
provider.provide(UserRepository, provides=IUserRepository, scope=Scope.APP)
provider.provide(ShopRepository, provides=IShopRepository, scope=Scope.APP)
provider.provide(
    FactoryRepository, provides=IFactoryRepository, scope=Scope.APP
)

provider.provide(MemoryEventBus, provides=IEventBus, scope=Scope.APP)

provider.provide(UCUser, scope=Scope.APP)
provider.provide(UCFactory, scope=Scope.APP)
provider.provide(UCShop, scope=Scope.APP)

dishka_container = make_async_container(provider)
