from aiogram import Router, F
from aiogram.types import Message
from bot import api


router = Router()


@router.message(F.text.startswith("promo-"))
async def promo(message: Message):
    promocode = message.text.split("promo-", 1)[1]
    get_promo = api.any("promo", f"{promocode}?uid={message.from_user.id}")
    exist = get_promo[""]
    if "detail" not in exist.keys():
        await message.answer(f"Успешно введен промокод :) {exist['message']}")
        await message.answer(f'Вы получаете {exist["money"]} очков')
    else:
        await message.answer(exist["detail"])
