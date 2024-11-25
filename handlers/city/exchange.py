from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import (
    CallbackQuery,
    Message,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)

from states import SellStolar
from bot import bot, api
from config import not_enough_points
from replys import rinok_markup, back_exchange

router = Router()


@router.callback_query(F.data == "рынок")
async def shop_stolar(call: CallbackQuery):
    await call.message.edit_text(
        "🌟 Добро пожаловать на рынок! 🌟 Я - торговец SC."
        "\n🪙 Я могу продать вам парочку за 1 млрд штука.🤩 \n"
        "Но если вам это не подходит, "
        "можете заглянуть на наш магазин @tegtoryshop для большего выбора. 🛍️🔥",
        reply_markup=rinok_markup,
    )


@router.callback_query(F.data == "sellonrinok")
async def sell_stolar_on_tegtory(call: CallbackQuery):
    await call.message.edit_text(
        "чтобы продать на @tegtoryshop пиши: продать",
        reply_markup=back_exchange,
    )


@router.message(F.text.lower().split()[0] == "продать")
async def sell_on_channel(message: Message, state: FSMContext):
    await message.answer(
        "Будет выставлен лот в канале @tegtoryshop.\n"
        "Введите количество SC на продажу, их сразу спишут"
    )
    await state.set_state(SellStolar.stolar_on_sell)


@router.message(StateFilter(SellStolar.stolar_on_sell))
async def set_stolar_for_sale(message: Message, state: FSMContext):
    amount = message.text
    player = api.player(message.from_user.id)

    if player.stolar < int(amount) or 0 > int(amount):
        return await message.answer("Недостаточно SC")

    player.stolar -= int(amount)
    await message.answer(
        "Введите цену за которую пользователи могут купить ваши SC\n"
        "Рекомендуется продать за: "
        f'{int(amount) * 1000000000:,} \nразрешено использовать "к" для обозначения тысячи'
    )
    await state.update_data(stolar_on_sell=amount)
    await state.set_state(SellStolar.money_buy)


@router.message(StateFilter(SellStolar.money_buy))
async def set_buy_price(message: Message, state: FSMContext):
    cost = message.text
    cost = cost.replace("к", "000").replace(",", "")
    if int(cost) < 0:
        return await message.answer("Не правильная цена")
    await state.update_data(money_buy=cost)
    await state.set_state(SellStolar.confirm)
    user = await state.get_data()
    cost = user["money_buy"]
    amount = user["stolar_on_sell"]
    await message.answer(
        'напишите "Да" если все верно\n'
        f"Количество: {amount}\n"
        f"Цена: {int(cost):,}"
    )


@router.message(StateFilter(SellStolar.confirm), F.text.lower() == "да")
async def create_message_sell(message: Message, state: FSMContext):
    user = await state.get_data()
    cost = user["money_buy"]
    amount = user["stolar_on_sell"]
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Купить",
                    callback_data=f"buy_stolar:{cost}:{amount}:{message.from_user.id}",
                )
            ]
        ]
    )
    await message.answer("Лот успешно создан можете проверять @tegtoryshop")
    await bot.send_message(
        "@tegtoryshop",
        f"продается {amount} SC за {int(cost):,} очков",
        reply_markup=markup,
    )
    await state.clear()


@router.callback_query(F.data.split(":")[0] == "buy_stolar")
async def buy_on_channel(call: CallbackQuery):
    data = call.data.split(":")
    player = api.player(call.from_user.id)
    money, stolar = player.get("money,stolar")
    if money < int(data[1]):
        return
    money -= int(data[1])
    stolar += int(data[2])
    player.set(
        {
            "telegram_id": call.from_user.id,
            "money": money,
            "stolar": stolar,
        }
    )
    api.player(data[3]).money += int(data[1])
    await bot.delete_message("@tegtoryshop", call.message.message_id)
    await bot.send_message(
        data[3],
        f"У вас купили SC {data[2]} на сумму {int(data[1]):,}",
    )
    await call.answer("Успешно", show_alert=True)


@router.callback_query(F.data.split(":")[0] == "buy_stolar_coin")
async def buy_stolar_coin(call: CallbackQuery):
    player = api.player(call.from_user.id)
    amount = int(call.data.split(":")[1])
    money, stolar = player.get("money,stolar")
    if money >= 1000000000 * amount:
        money -= 1000000000 * amount
        stolar += 1 * amount
        player.set(
            {
                "telegram_id": call.from_user.id,
                "money": money,
                "stolar": stolar,
            }
        )
        await call.message.edit_text(
            f"куплено {amount} SC за {1000000000 * amount}",
            reply_markup=back_exchange,
        )
    else:
        await call.answer(not_enough_points, show_alert=True)
