import time
from unittest.mock import AsyncMock, MagicMock

import pytest

from domain.commands.user import RegisterUserCommand, StartUserWorkCommand
from domain.entities import Factory, Product, User
from domain.interfaces import UserRepository
from domain.results import Failure, Success
from domain.use_cases.commands.user import (
    RegisterUserCommandHandler,
    StartUserWorkCommandHandler,
)
from domain.use_cases.user import UserEvent


@pytest.fixture
def user_repo() -> MagicMock:
    repo = MagicMock(spec=UserRepository)
    repo.create = AsyncMock()
    repo.update = AsyncMock()
    repo.get = AsyncMock()
    return repo


@pytest.fixture
def event_bus() -> MagicMock:
    bus = MagicMock()
    bus.emit = AsyncMock()
    return bus


@pytest.mark.asyncio
async def test_create_user(user_repo: MagicMock) -> None:
    expected_result = User(username="test", name="test", id=1)
    user_repo.create.return_value = expected_result

    query = RegisterUserCommandHandler(user_repo)
    result = await query(
        RegisterUserCommand(username="test", name="test", user_id=1)
    )

    assert isinstance(result, Success)
    assert isinstance(result.data, User)

    user_repo.create.assert_called_once_with(expected_result)


@pytest.mark.asyncio
async def test_subtract_money(user_repo: MagicMock) -> None:
    event = UserEvent(user_repo, MagicMock())
    user = User(id=1, name="User", username="user", money=100)
    await event._subtract_user_money({"user": user, "amount": 30})

    assert user.money == 100 - 30
    user_repo.update.assert_called_once_with(user)


@pytest.mark.asyncio
async def test_start_user_work(
    user_repo: MagicMock, event_bus: MagicMock
) -> None:
    handler = StartUserWorkCommandHandler(user_repo, event_bus)

    cmd = StartUserWorkCommand(
        user=User(id=1, name="User", username="user", money=100),
        factory=Factory(id=1, name="Factory"),
        time=1,
        product=Product(name=""),
    )
    result = await handler(cmd)

    assert isinstance(result, Success)
    event_bus.emit.assert_called_once()
    user_repo.update.assert_called_once()


@pytest.mark.asyncio
async def test_start_user_work_failed_already_working(
    user_repo: MagicMock, event_bus: MagicMock
) -> None:
    handler = StartUserWorkCommandHandler(user_repo, event_bus)
    now = time.time()
    cmd = StartUserWorkCommand(
        user=User(
            id=1,
            name="User",
            username="user",
            money=100,
            end_work_time=now * 2,
        ),
        factory=Factory(id=1, name="Factory"),
        time=1,
        product=Product(name=""),
    )
    result = await handler(cmd)

    assert isinstance(result, Failure)
    event_bus.emit.assert_not_called()
    user_repo.update.assert_not_called()
