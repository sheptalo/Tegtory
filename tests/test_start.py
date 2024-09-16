from handlers import start
import pytest
from unittest.mock import AsyncMock


@pytest.mark.asyncio
async def test_cancel():
    state = AsyncMock()
    message = AsyncMock()
    await start.cancel(message, state)
    state.clear.assert_called()
    message.answer.assert_called_once_with('отменено')


@pytest.mark.asyncio
async def test_start():
    message = AsyncMock()
    await start.start(message)
    message.answer.assert_called()


@pytest.mark.asyncio
async def test_check_text():
    message = AsyncMock()
    await start.check_text(message)
    message.answer.assert_called()