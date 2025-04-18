from unittest.mock import AsyncMock, MagicMock

import pytest

from common import settings
from common.exceptions import (
    NotEnoughPointsException,
)
from common.settings import TAX_LIMIT
from domain.context.factory import StartWorkContext, UserFactoryContext
from domain.entity import Factory, Product, Storage, StorageProduct, User
from domain.entity.factory import StartFactoryEvent
from domain.events import EventType
from domain.interfaces import IFactoryRepository
from domain.use_cases.factory import UCFactory


@pytest.fixture
def factory_repo():
    repo = MagicMock(spec=IFactoryRepository)
    repo.get = MagicMock()
    repo.get_storage = MagicMock()
    repo.create = MagicMock()
    repo.update = MagicMock()
    repo.by_name = MagicMock()
    repo.add_available_product = MagicMock()
    repo.create_storage = MagicMock(return_value=Storage(id=1))
    repo.get_available_products = MagicMock()
    repo.update_storage = MagicMock()
    repo.add_product_in_storage = MagicMock()
    return repo


@pytest.fixture
def event_bus():
    bus = MagicMock()
    bus.emit = AsyncMock()
    return bus


@pytest.fixture
def uc_factory(factory_repo, event_bus):
    return UCFactory(factory_repo, event_bus)


@pytest.mark.asyncio
async def test_get_factory_with_storage(uc_factory, factory_repo):
    test_factory = Factory(id=1, name="")
    factory_repo.get.return_value = test_factory
    factory_repo.get_storage.return_value = Storage(id=1)

    result = await uc_factory.get(1)

    factory_repo.get.assert_called_once_with(1)
    factory_repo.get_storage.assert_called_once_with(test_factory)
    assert result.storage


@pytest.mark.asyncio
async def test_create_new_factory(uc_factory, factory_repo):
    test_factory = Factory(id=1, name="New Factory")
    factory_repo.get.return_value = None
    factory_repo.by_name.return_value = None

    await uc_factory.create(test_factory)

    factory_repo.create.assert_called_once_with(test_factory)
    assert factory_repo.add_available_product.call_count == len(
        settings.DEFAULT_AVAILABLE_PRODUCTS
    )


@pytest.mark.asyncio
async def test_pay_tax_success(uc_factory, factory_repo, event_bus):
    ctx = UserFactoryContext(
        user=User(money=1000, username="", name="", id=1),
        factory=Factory(tax=500, name="", id=1),
    )

    await uc_factory.pay_tax(ctx)

    assert ctx.factory.tax == 0
    factory_repo.update.assert_called_once_with(ctx.factory)
    event_bus.emit.assert_awaited_once_with(
        EventType.SubtractMoney, user=ctx.user, amount=500
    )


@pytest.mark.asyncio
async def test_upgrade_failure_low_balance(uc_factory):
    ctx = UserFactoryContext(
        user=User(money=50, username="", name="", id=1),
        factory=Factory(name="", id=1),
    )

    result = await uc_factory.upgrade(ctx)
    assert "Недостаточно" in result

@pytest.mark.asyncio
async def test_hire_worker_max_limit(uc_factory):
    ctx = UserFactoryContext(
        user=User(money=10000, username="", name="", id=1),
        factory=Factory(name="", id=1),
    )

    result = await uc_factory.hire(ctx)
    assert "Максимальное количество" in str(result)


@pytest.mark.asyncio
async def test_start_factory_event_flow(uc_factory, factory_repo, event_bus):
    test_product = Product(name="Test")
    data = StartFactoryEvent(
        factory=Factory(storage=Storage(), name="", id=1),
        product=test_product,
        time=test_product.time_to_create,
    )

    await uc_factory.start_factory_event(data)

    factory_repo.update.assert_called_once_with(data.factory)
    factory_repo.add_product_in_storage.assert_called_once_with(
        StorageProduct(
            product=test_product,
            storage=data.factory.storage,
            amount=1,
        )
    )
    event_bus.emit.assert_awaited_once_with(
        EventType.EndFactoryWork, factory=data.factory, stock=1
    )


@pytest.mark.asyncio
async def test_start_factory_tax_limit_exceeded(uc_factory):
    ctx = StartWorkContext(
        factory=Factory(tax=TAX_LIMIT + 1, name="", id=1),
        user=User(username="", name="", id=1),
        product=Product(name=""),
        time=8.0,
    )

    result = await uc_factory.start_factory(ctx)
    assert result == "Выплатите Налоги чтобы продолжить"


@pytest.mark.asyncio
async def test_upgrade_storage_flow(uc_factory, factory_repo, event_bus):
    test_storage = Storage()
    test_user = User(money=3000, username="", name="", id=1)

    result = await uc_factory.upgrade_storage(test_storage, test_user)

    max_stock = Storage().max_stock + 10
    assert result.max_stock == max_stock
    factory_repo.update_storage.assert_called_once_with(test_storage)
    event_bus.emit.assert_awaited_once_with(
        EventType.SubtractMoney, amount=Storage().upgrade_price, user=test_user
    )
