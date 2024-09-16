import pytest

from handlers import user
from unittest.mock import AsyncMock


@pytest.mark.asyncio
async def test_spam():
    message = AsyncMock()
    await user.stop_spam(message)
    message.answer.assert_called_with('Не спамьте!')


@pytest.mark.asyncio
async def test_subscribe():
    message = AsyncMock()
    await user.subscribe(message)
    message.answer.assert_called()


@pytest.mark.asyncio
async def test_subscribe_call():
    call = AsyncMock()
    await user.subscribe_call(call)
    call.message.edit_text.assert_called()


    from aiogram.exceptions import TelegramBadRequest

    def err(*args, **kwargs):
        raise TelegramBadRequest(AsyncMock(), AsyncMock())
    call = AsyncMock()
    call.message.edit_text = err

    await user.subscribe_call(call)

    call.message.delete.assert_called()


@pytest.mark.asyncio
async def test_profile():
    call = AsyncMock()
    call.from_user.id = 123456789

    await user.profile(call)
    call.message.answer.assert_called()

    message = AsyncMock()
    message.from_user.id = 123456789
    await user.balance(message)


@pytest.mark.asyncio
async def test_change_nick():
    message = AsyncMock()
    message.from_user.id = 123456789
    state = AsyncMock()
    await user.change_nick(message, state)
    message.answer.assert_called()

    from States import ChangeNick
    state.set_state.assert_called_with(ChangeNick.new_nickname)


@pytest.mark.asyncio
async def test_confirm_changes():
    message = AsyncMock()
    message.from_user.id = 123456789
    message.text = '123456789012345678901234567890'
    state = AsyncMock()
    await user.confirm_changes(message, state)

    message.answer.assert_not_called()


@pytest.mark.asyncio
async def test_subscribe_check():
    def raise_exception():
        raise BaseException

    call = AsyncMock()
    await user.subscribe_check(call)

    call.message.delete.assert_called()
    call.message.answer.assert_called()

    call.message.delete = raise_exception()

    await user.subscribe_check(call)
    call.message.answer.assert_not_called()
