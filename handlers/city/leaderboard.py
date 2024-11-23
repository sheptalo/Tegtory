from aiogram import F, Router, types
from aiogram.exceptions import TelegramBadRequest

from Filters import LeaderboardFilter
from middlewares.UserMiddleWare import UserMiddleWare
from bot import api
from db import Leaderboard
from replys import leaderboard_inline, old_seasons_markup

router = Router()
router.message.middleware(UserMiddleWare())
pre_alpha_season_leader = (
    "Таблица лидеров: \n"
    "1. название фабрики: nagan. Баланс 40250 очков. \n\n"
    "2. название фабрики: ffffff. Баланс 14550 очков. \n\n"
    "3. название фабрики: Смелая?. Баланс 9500 очков. \n\n"
    "4. название фабрики: MAXXXlox. Баланс 4799 очков. \n\n"
    "5. название фабрики: Самир. Баланс 1750 очков. \n\n"
    "6. название фабрики: @#$та. Баланс 800 очков. \n\n"
    "7. название фабрики: к$н$мен. Баланс 600 очков. \n\n"
    "8. название фабрики: alfheisj. Баланс 600 очков.\n\n "
    "9. название фабрики: шептало. Баланс 200 очков."
)
alpha_season = """
🏆 Таблица лидеров 🏆
🥇1. Название фабрики: я ваш бог👹
Баланс: 990,289,427,000,000 очков. 

🥈2. Название фабрики: кишлэк
Баланс: 194,906,656,980,779 очков. 

🥉3. Название фабрики: СтатьяУКРФ
Баланс: 5,009,446,491,134 очков. 

4. Название фабрики: pidorasi
Баланс: 675,000,000.5 очков. 

5. Название фабрики: сюда
Баланс: 7,583 очков. 
"""


@router.callback_query(F.data == "leaderboard")
async def leaderboard(call: types.CallbackQuery):
    try:
        await call.message.edit_text(
            f"{Leaderboard().Money()}"
            f"\n\nваше место в топе {Leaderboard().Money().me(api.player(call.from_user.id).id)}",
            reply_markup=leaderboard_inline,
        )
    except TelegramBadRequest:
        pass


@router.message(LeaderboardFilter())
async def leaderboard_def(message: types.Message):
    try:
        await message.answer(
            f"{Leaderboard().Money()}"
            f"\n\nваше место в топе {Leaderboard().Money().me(api.player(message.from_user.id).id)}",
            reply_markup=leaderboard_inline,
        )
    except TelegramBadRequest:
        pass


@router.callback_query(F.data == "rating_leaderboard")
async def call_rating_leaderboard(call: types.CallbackQuery):
    try:
        await call.message.edit_text(
            f"{Leaderboard().Rating()}"
            f"\n\nВаше место в топе {Leaderboard().Rating().me(api.player(call.from_user.id).id)}",
            reply_markup=leaderboard_inline,
        )
    except TelegramBadRequest:
        pass


@router.callback_query(F.data == "stolar_leaderboard")
async def call_stolar_leaderboard(call: types.CallbackQuery):
    try:
        await call.message.edit_text(
            str(Leaderboard().Stolar())
            + f"\n\nВаше место в топе {Leaderboard().Stolar().me(api.player(call.from_user.id).id)}",
            reply_markup=leaderboard_inline,
        )
    except TelegramBadRequest:
        pass


@router.callback_query(F.data == "factory_leaderboard")
async def call_level_leaderboard(call: types.CallbackQuery):
    try:
        await call.message.edit_text(
            str(Leaderboard().Level())
            + f"\n\nВаше место в топе {Leaderboard().Level().me(api.player(call.from_user.id).id)}",
            reply_markup=leaderboard_inline,
        )
    except TelegramBadRequest as e:
        print(e)


@router.callback_query(F.data == "eco_leaderboard")
async def call_clan_leaderboard(call: types.CallbackQuery):
    try:
        await call.message.edit_text(
            str(Leaderboard().Eco())
            + f"\n\nВаше место в топе {Leaderboard().Eco().me(api.player(call.from_user.id).id)}",
            reply_markup=leaderboard_inline,
        )
    except TelegramBadRequest as e:
        print(e)


@router.callback_query(F.data == "clan_leaderboard")
async def call_clan_leaderboard(call: types.CallbackQuery):
    try:
        await call.message.edit_text(
            str(Leaderboard().Clans()), reply_markup=leaderboard_inline
        )
    except TelegramBadRequest:
        pass


@router.callback_query(F.data == "pre_apha_season")
async def pre_alpha_leaderboard(call: types.CallbackQuery):
    try:
        await call.message.edit_text(
            pre_alpha_season_leader, reply_markup=leaderboard_inline
        )
    except TelegramBadRequest:
        pass


@router.callback_query(F.data == "alpha_season")
async def pre_alpha_leaderboard(call: types.CallbackQuery):
    try:
        await call.message.edit_text(
            alpha_season, reply_markup=leaderboard_inline
        )
    except TelegramBadRequest:
        pass


@router.callback_query(F.data == "old_leaderboard")
async def call_clan_leaderboard(call: types.CallbackQuery):
    try:
        await call.message.edit_text(
            "Здесь вы можете посмотреть лидеров прошлых сезонов\n"
            "*Заметка* дизайн прошлых версий специально сохранен.\n"
            "*заметка 2* некоторые имена могут изменены если содержат нецензурные выражения.",
            reply_markup=old_seasons_markup,
        )
    except TelegramBadRequest:
        pass
