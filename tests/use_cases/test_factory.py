from unittest.mock import AsyncMock, MagicMock

import pytest

from domain.commands.factory import CreateFactoryCommand
from domain.entities import Factory, Storage
from domain.interfaces import FactoryRepository
from domain.queries.factory import GetFactoryQuery
from domain.results import Success
from domain.use_cases.commands.factory import CreateFactoryHandler
from domain.use_cases.factory import UCFactory
from domain.use_cases.queries.factory import GetFactoryQueryHandler


@pytest.fixture
def factory_repo():
    repo = MagicMock(spec=FactoryRepository)
    repo.get = AsyncMock()
    repo.get_storage = AsyncMock()
    repo.create = AsyncMock()
    repo.update = AsyncMock()
    repo.by_name = AsyncMock()
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
async def test_get_factory(factory_repo):
    factory_repo.get.return_value = Factory(id=1, name="")
    factory_repo.get_storage.return_value = Storage()
    query_handler = GetFactoryQueryHandler(factory_repo)
    result = await query_handler(GetFactoryQuery(factory_id=1))

    factory_repo.get.assert_called_once_with(1)
    assert isinstance(result, Success)


@pytest.mark.asyncio
async def test_create_new_factory(factory_repo):
    async def wrap(s):
        return None

    factory_repo.by_name = wrap

    command_handler = CreateFactoryHandler(factory_repo, AsyncMock())
    await command_handler(CreateFactoryCommand(name="1", id=1))

    factory_repo.create.assert_called_once_with(Factory(name="1", id=1))
