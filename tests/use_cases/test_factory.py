from unittest.mock import MagicMock

import pytest

from domain.use_cases import UCFactory


@pytest.fixture
def factory_repository():
    mock = MagicMock()
    return mock


@pytest.fixture
def mock_factory():
    mock = MagicMock()
    mock.id = 1
    mock.name = "Test"
    return mock


@pytest.mark.asyncio
async def test_create_factory(factory_repository, mock_factory):
    factory_repository.get.return_value = None
    factory_repository.by_name.return_value = None
    factory_repository.create.return_value = mock_factory

    await UCFactory(factory_repository, MagicMock()).create(mock_factory)

    factory_repository.create.assert_called_with(
        mock_factory.name, mock_factory.id
    )
