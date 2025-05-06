from unittest.mock import AsyncMock, Mock

import pytest

from domain.commands import UpgradeStorageCommand
from domain.entities import Storage
from domain.queries import GetStorageQuery
from domain.results import Success
from domain.use_cases.commands.storage import UpgradeStorageCommandHandler
from domain.use_cases.queries.factory import GetStorageQueryHandler


@pytest.mark.asyncio
async def test_get_storage(storage_repository: Mock) -> None:
    handler = GetStorageQueryHandler(storage_repository)
    result = await handler(GetStorageQuery(factory_id=1))

    assert isinstance(result, Success)
    storage_repository.get.assert_called_with(1)


@pytest.mark.asyncio
async def test_upgrade_storage_success(storage_repository: Mock) -> None:
    handler = UpgradeStorageCommandHandler(storage_repository, AsyncMock())
    result = await handler(
        UpgradeStorageCommand(
            storage=Storage(), user_id=1, user_money=1000, factory_id=1
        )
    )

    assert isinstance(result, Success)
    storage_repository.upgrade.assert_called_with(1)
