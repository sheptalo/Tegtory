from unittest.mock import AsyncMock, MagicMock

import pytest

from domain.context.factory import StartWorkContext
from domain.entity import Factory, Product, User
from domain.entity.factory import StartFactoryEvent
from domain.events import EventType, IEventBus
from domain.interfaces import UserRepository
from domain.use_cases.user import UCUser


@pytest.fixture
def user_repo():
    repo = MagicMock(spec=UserRepository)
    repo.create = MagicMock()
    repo.update = MagicMock()
    repo.get = MagicMock()
    return repo


@pytest.fixture
def event_bus():
    bus = MagicMock(spec=IEventBus)
    bus.emit = AsyncMock()
    return bus


@pytest.fixture
def uc_user(user_repo, event_bus):
    return UCUser(user_repo, event_bus)


@pytest.mark.asyncio
async def test_create_user(uc_user, user_repo):
    test_user = User(id=1, name="Test", username="test_user")
    await uc_user.create(test_user)

    user_repo.create.assert_called_once_with(test_user)


@pytest.mark.asyncio
async def test_start_work_when_user_free(uc_user, user_repo, event_bus):
    user = User(id=1, name="User", username="user", state=False)
    factory = Factory(id=1, name="factory")
    product = Product(id=1, name="lol")
    ctx = StartWorkContext(
        user=user, factory=factory, product=product, time=8.5
    )

    await uc_user.start_work(ctx)

    user_repo.update.assert_called_once_with(user)

    event_bus.emit.assert_awaited_once_with(
        EventType.StartFactory,
        data=StartFactoryEvent(factory=factory, time=8.5, product=product),
    )


@pytest.mark.asyncio
async def test_subtract_money(uc_user, user_repo):
    user = User(id=1, name="User", username="user", money=100)
    await uc_user._subtract_user_money(user, 30)

    assert user.money == 70
    user_repo.update.assert_called_once_with(user)
