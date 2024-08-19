from aiogram import Router, types, F
from aiogram.filters import Command

from MIddleWares.UserMiddleWare import UserMiddleWare

from config import clan_lvl, create_clan_text, not_in_clan, not_enough_points

from db.Factory import Factory
from db.Player import Player
from db.leaderboard import Leaderboard

router = Router()
router.message.middleware(UserMiddleWare())


@router.message(F.text.lower() == 'объединение')
async def clan_def(message: types.Message):
    player = Player(message.from_user.id)
    clan = player.clan
    if clan.name == '':
        return await message.answer(not_in_clan, parse_mode='HTML')
    _text = f'🏆 *Лидеры Объединения \"{clan.name}\"* 🏆\n\n'
    _text += str(Leaderboard().Clan(clan.name))
    _text += f'💰Вклад в объединение {player.money:,}\n\n'
    if bool(clan.leader):
        _text += '👑*Вы основатель* этого объединения\n'

    _text += (f'\nПокинуть Объединение - */leave*'
              f'\nСсылка на вступление в объединение - `/join "{clan.name}"`')
    await message.answer(_text, parse_mode='Markdown')


@router.message(Command('leave'))
async def leave_clan_cm(message: types.Message):
    player = Player(message.from_user.id)
    player.clan.name = ''
    player.clan.leader = 0
    await message.answer('Ты покинул обьединение')


@router.message(Command('join'))
async def join(message: types.Message):
    factory = Factory(message.from_user.id)
    if factory.level < 10:
        return await message.answer(clan_lvl)
    try:
        name = message.text.split()[1]
    except:
        return await message.answer('Не указано название объединения для вступления')
    name = name.replace('"', '')
    player = Player(message.from_user.id)
    clan = player.clan
    if clan.name != '':
        return await message.answer('Вы уже в объединении')

    if not clan.exists(name):
        return await message.answer("Объединения не существует")

    clan.name = name
    await message.answer('Поздравляю вы в объединении')


@router.message(Command('create_clan'))
async def create_clan(message: types.Message):
    factory = Factory(message.from_user.id)
    player = Player(message.from_user.id)
    if factory.level < 10:
        return await message.answer(clan_lvl)
    try:
        clan_name = message.text.split()[1]
    except:
        return await message.answer(create_clan_text, parse_mode='HTML')

    if not player.clan.can_create(clan_name):
        return await message.answer('Такое объединение уже существует')

    if len(clan_name) > 100:
        return await message.answer(create_clan_text, parse_mode='HTML')

    if player.clan.name != '':
        return await message.answer('Вы уже состоите в объединении')

    if player.money > 7500:
        player.money -= 7500
        player.clan.name = clan_name
        player.clan.leader = 1
        await message.answer(f'Успешно создано обьединение {clan_name}')
    else:
        await message.answer(not_enough_points)

# endregion
