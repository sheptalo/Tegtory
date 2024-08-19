from aiogram import Router, types, F

from Filters import SubscribeFilter, SpamFilter, SpamFilterCallBack
from MIddleWares.UserMiddleWare import UserMiddleWare
from replys import subscribed_channel

router = Router()
router.message.middleware(UserMiddleWare())


@router.message(SubscribeFilter())
async def not_subscribed(message: types.Message):
    await message.answer('Подпишитесь на канал @tegtory чтобы пользоваться ботом',
                         reply_markup=subscribed_channel)


@router.message(SpamFilter(), F.text)
async def not_subscribed(message: types.Message):
    await message.answer('Не спамьте!')
    await message.delete()


@router.message(SpamFilterCallBack(), F.data)
async def not_subscribed(call: types.CallbackQuery):
    return 0

