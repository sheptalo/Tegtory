from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from replys import shop_reply
from handlers.city import router as shop

router = Router()
router.include_router(shop)

shop_text = ('🎁🔥 Добро пожаловать в магазин! Здесь вы можете '
             'приобрести билеты для участия в лотерееи многое другое! 🏪💸\n'
             '💰🎉 Желаем вам удачных покупок и больших выигрышей! ')


@router.callback_query(F.data == 'back_shop')
async def back_shop(call: CallbackQuery, state: FSMContext):
    await state.clear()
    await call.message.edit_text(shop_text,
                                 reply_markup=shop_reply)


@router.callback_query(F.data == 'shop')
async def shop_main(call: types.CallbackQuery):
    text = '\n'
    if call.message.chat.type != 'private':
        text += ("🟥При покупке товаров связанных с фабрикой они будут *покупаться для фабрики группы*, "
                 "для покупки товаров для *своей фабрики* покупайте в личных сообщениях с ботом!!🟥")
    await call.message.edit_text(shop_text + text, reply_markup=shop_reply, parse_mode='Markdown')
