from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message
from bot import api
from replys import prices

router = Router()


@router.callback_query(F.data == "донат")
async def donate(call: CallbackQuery):
    await call.message.answer(
        "Страница доната:\nВозможность возврата не предусмотрена"
    )
    await call.message.answer_invoice(
        "1,000 очков",
        "Закончились деньги? приобрети 1,000 очков прямо сейчас. Без возврата",
        "donate",
        provider_token="",
        currency="XTR",
        prices=prices,
    )


@router.pre_checkout_query()
async def pre_checkout_query(query: CallbackQuery):
    await query.answer(ok=True)


@router.message(F.successful_payment)
async def payment(message: Message):
    api.player(message.from_user.id).money += 1000
    await message.answer("Успешная транзакция")


@router.message(Command("paysupport"))
async def paysupport(message: Message):
    await message.answer("За донат возможность возврата не предусмотрена")
