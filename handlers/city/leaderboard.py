from aiogram import F, Router, types
from aiogram.exceptions import TelegramBadRequest

from Filters import LeaderboardFilter
from MIddleWares.UserMiddleWare import UserMiddleWare
from config import pre_alpha_season_leader, alpha_season
from db.Player import Player
from db.leaderboard import Leaderboard
from replys import leaderboard_inline, old_seasons_markup

router = Router()
router.message.middleware(UserMiddleWare())


@router.callback_query(F.data == 'leaderboard')
async def leaderboard(call: types.CallbackQuery):
    try:
        await call.message.edit_text(f'{Leaderboard().Money()}'
                                     f'\n\nваше место в топе {Leaderboard().Money().me(Player(call.from_user.id).iternal_id)}',
                                     reply_markup=leaderboard_inline)
    except TelegramBadRequest as e:
        pass


@router.message(LeaderboardFilter())
async def leaderboard_def(message: types.Message):
    try:
        await message.answer(f'{Leaderboard().Money()}'
                             f'\n\nваше место в топе {Leaderboard().Money().me(Player(message.from_user.id).iternal_id)}',
                             reply_markup=leaderboard_inline)
    except TelegramBadRequest as e:
        pass


@router.callback_query(F.data == 'rating_leaderboard')
async def call_rating_leaderboard(call: types.CallbackQuery):
    try:
        await call.message.edit_text(f'{Leaderboard().Rating()}'
                                     f'\n\nВаше место в топе {Leaderboard().Rating().me(Player(call.from_user.id).iternal_id)}',
                                     reply_markup=leaderboard_inline)
    except TelegramBadRequest as e:
        pass


@router.callback_query(F.data == 'stolar_leaderboard')
async def call_stolar_leaderboard(call: types.CallbackQuery):
    try:
        await call.message.edit_text(str(Leaderboard().Stolar()) +
                                     f'\n\nВаше место в топе {Leaderboard().Stolar().me(Player(call.from_user.id).iternal_id)}',
                                     reply_markup=leaderboard_inline)
    except TelegramBadRequest as e:
        pass


@router.callback_query(F.data == 'factory_leaderboard')
async def call_clan_leaderboard(call: types.CallbackQuery):
    try:
        await call.message.edit_text(str(Leaderboard().Level()) +
                                     f'\n\nВаше место в топе {Leaderboard().Level().me(Player(call.from_user.id).iternal_id)}',
                                     reply_markup=leaderboard_inline)
    except TelegramBadRequest as e:
        pass


@router.callback_query(F.data == 'eco_leaderboard')
async def call_clan_leaderboard(call: types.CallbackQuery):
    try:
        await call.message.edit_text(str(Leaderboard().Eco()) +
                                     f'\n\nВаше место в топе {Leaderboard().Eco().me(Player(call.from_user.id).iternal_id)}',
                                     reply_markup=leaderboard_inline)
    except TelegramBadRequest as e:
        pass


@router.callback_query(F.data == 'clan_leaderboard')
async def call_clan_leaderboard(call: types.CallbackQuery):
    await call.message.edit_text(str(Leaderboard().Clans()), reply_markup=leaderboard_inline)


@router.callback_query(F.data == 'pre_apha_season')
async def pre_alpha_leaderboard(call: types.CallbackQuery):
    try:
        await call.message.edit_text(pre_alpha_season_leader, reply_markup=leaderboard_inline)
    except TelegramBadRequest as e:
        pass


@router.callback_query(F.data == 'alpha_season')
async def pre_alpha_leaderboard(call: types.CallbackQuery):
    try:
        await call.message.edit_text(alpha_season, reply_markup=leaderboard_inline)
    except TelegramBadRequest as e:
        pass


@router.callback_query(F.data == 'old_leaderboard')
async def call_clan_leaderboard(call: types.CallbackQuery):
    try:
        await call.message.edit_text('Здесь вы можете посмотреть лидеров прошлых сезонов\n'
                                     '*Заметка* дизайн прошлых версий специально сохранен.\n'
                                     '*заметка 2* некоторые имена могут изменены если содержат нецензурные выражения.',
                                     reply_markup=old_seasons_markup)
    except TelegramBadRequest as e:
        pass
