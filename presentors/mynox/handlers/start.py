from aiogram import F, Router, types
from aiogram.filters import CommandStart, StateFilter
from aiogram.fsm.context import FSMContext

from ..kb.menu import menu_markup
from ..states.mine import MineStates

router = Router()


@router.callback_query(F.data == "menu")
async def call_menu(call: types.CallbackQuery, state: FSMContext):
    await state.clear()
    await call.message.edit_media(
        media=types.InputMediaPhoto(
            media="",
            caption=f"Твоя шахта заждалась тебя {call.from_user.first_name}\n"
            f"Ты в меню. Куда направимся?",
        ),
        reply_markup=menu_markup,
    )


@router.message(CommandStart())
async def start_command(message: types.Message, state: FSMContext):
    mine = None
    if not mine:
        await message.answer(
            "Привет! Это Mynox. Твой друг на пути к славе..... по добыче руды."
        )
        await message.answer(
            "Давай я помогу тебе начать игру, придумай название для своей шахты"
        )
        return await state.set_state(MineStates.create_mine)
    await state.clear()
    await message.answer_photo(
        "",
        f"Твоя шахта заждалась тебя {message.from_user.first_name}\n"
        f"Ты в меню. Куда направимся?",
        reply_markup=menu_markup,
    )


@router.message(StateFilter(MineStates.create_mine))
async def creating_mine(message: types.Message, state: FSMContext):
    await message.answer("""
Успешно, твоя шахта ждет тебя,
а в качестве подарка я прокопал и зарегистрировал для тебя твой *первый туннель*.

*Туннель* - Место где будет происходить твоя основная работа, у каждого туннеля есть свой уникальный номер,
по которому ее можно отличить. В туннеле твои рабочие, или ты сам, добываешь различные ископаемые.

Существует множество ископаемых, но чтобы начать их добывать необходимо их исследовать, сейчас для тебя доступен только
Уголь. Улучшай туннели, покупай оборудование, нанимай сотрудников, позаботься об их безопасности и делай все чтобы стать
*самым богатым владельцем шахты*
""")
    await state.clear()
    await start_command(message, state)
