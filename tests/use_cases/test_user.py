from unittest.mock import AsyncMock, MagicMock

import pytest

from domain.commands.user import RegisterUserCommand
from domain.entities import User
from domain.interfaces import UserRepository
from domain.results import Success
from domain.use_cases.commands.user import RegisterUserCommandHandler
from domain.use_cases.user import UCUser


@pytest.fixture
def user_repo():
    repo = MagicMock(spec=UserRepository)
    repo.create = AsyncMock()
    repo.update = AsyncMock()
    repo.get = AsyncMock()
    return repo


@pytest.fixture
def event_bus():
    bus = MagicMock()
    bus.emit = AsyncMock()
    return bus


@pytest.fixture
def uc_user(user_repo, event_bus):
    return UCUser(user_repo, event_bus)


@pytest.mark.asyncio
async def test_create_user(user_repo):
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
async def test_subtract_money(uc_user, user_repo):
    user = User(id=1, name="User", username="user", money=100)
    await uc_user._subtract_user_money({"user": user, "amount": 30})

    assert user.money == 70
    user_repo.update.assert_called_once_with(user)
