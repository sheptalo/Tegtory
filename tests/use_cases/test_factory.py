from unittest.mock import AsyncMock, MagicMock

import pytest

from domain.commands.factory import CreateFactoryCommand, HireWorkerCommand
from domain.entities import Factory, Storage
from domain.interfaces import FactoryRepository
from domain.queries.factory import GetFactoryQuery
from domain.results import Failure, Success
from domain.use_cases.commands.factory import (
    CreateFactoryHandler,
    HireWorkerCommandHandler,
)
from domain.use_cases.queries.factory import GetFactoryQueryHandler


@pytest.fixture
def factory_repo() -> MagicMock:
    repo = MagicMock(spec=FactoryRepository)
    repo.get = AsyncMock()
    repo.get_storage = AsyncMock()
    repo.create = AsyncMock()
    repo.update = AsyncMock()
    repo.hire = AsyncMock()
    repo.by_name = AsyncMock()
    return repo


@pytest.fixture
def event_bus() -> MagicMock:
    bus = MagicMock()
    bus.emit = AsyncMock()
    return bus


@pytest.mark.asyncio
async def test_get_factory(factory_repo: MagicMock) -> None:
    factory_repo.get.return_value = Factory(id=1, name="")
    factory_repo.get_storage.return_value = Storage()
    query_handler = GetFactoryQueryHandler(factory_repo)
    result = await query_handler(GetFactoryQuery(factory_id=1))

    factory_repo.get.assert_called_once_with(1)
    assert isinstance(result, Success)


@pytest.mark.asyncio
async def test_create_new_factory(factory_repo: MagicMock) -> None:
    factory_repo.by_name.return_value = None

    command_handler = CreateFactoryHandler(factory_repo, AsyncMock())
    await command_handler(CreateFactoryCommand(name="1", id=1))

    factory_repo.create.assert_called_once_with(Factory(name="1", id=1))


@pytest.mark.asyncio
async def test_create_new_factory_failed(factory_repo: MagicMock) -> None:
    factory_repo.by_name.return_value = Factory(id=1, name="")

    command_handler = CreateFactoryHandler(factory_repo, AsyncMock())
    result = await command_handler(CreateFactoryCommand(name="1", id=1))

    factory_repo.by_name.assert_called_once_with("1")
    assert isinstance(result, Failure)


@pytest.mark.asyncio
async def test_hire_worker_success(factory_repo: MagicMock) -> None:
    command_handler = HireWorkerCommandHandler(factory_repo, AsyncMock())
    result = await command_handler(
        HireWorkerCommand(
            factory=Factory(
                name="1", id=1, level=100, workers=0, end_work_time=0
            ),
            user_id=1,
            user_money=10000,
        )
    )

    factory_repo.hire.assert_called_once_with(1)
    assert isinstance(result, Success)


@pytest.mark.asyncio
async def test_hire_worker_failure_insufficient_money(
    factory_repo: MagicMock,
) -> None:
    command_handler = HireWorkerCommandHandler(factory_repo, AsyncMock())
    result = await command_handler(
        HireWorkerCommand(
            factory=Factory(name="1", id=1, level=100, workers=80),
            user_id=1,
            user_money=0,
        )
    )
    assert isinstance(result, Failure)


@pytest.mark.asyncio
async def test_hire_worker_failure_max_workers(
    factory_repo: MagicMock,
) -> None:
    command_handler = HireWorkerCommandHandler(factory_repo, AsyncMock())
    result = await command_handler(
        HireWorkerCommand(
            factory=Factory(name="1", id=1, level=1, workers=1),
            user_id=1,
            user_money=1770,
        )
    )
    assert isinstance(result, Failure)
    assert result.reason == "Вы достигли лимита рабочих для данного уровня"
