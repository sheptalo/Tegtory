from unittest.mock import MagicMock

import pytest

from domain.use_cases import UCUser


@pytest.mark.asyncio
async def test_register_user(mock_user):
    mock = MagicMock()
    mock.create.return_value = mock_user
    use_case = UCUser(mock, MagicMock())
    result = await use_case.create(mock_user)
    mock.create.assert_called_once_with(1, "Test User", "testuser")
    assert result == mock_user
