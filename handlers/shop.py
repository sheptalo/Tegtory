from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from MIddleWares.UserMiddleWare import UserMiddleWare
from config import shop_text
from replys import shop_reply
from handlers.city import router as shop

router = Router()
router.message.middleware(UserMiddleWare())
router.include_router(shop)


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
