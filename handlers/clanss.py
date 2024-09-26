from aiogram import Router, types, F
from aiogram.filters import Command

from MIddleWares.UserMiddleWare import UserMiddleWare
from api import api

from config import not_enough_points
from db import Leaderboard
from replys import back_city

router = Router()
router.message.middleware(UserMiddleWare())

clan_lvl = 'Для создания/вступления в обьединение необходимо иметь 10 уровень фабрики'
create_clan_text = (f'Чтобы создать обьединение и захватывать мир с друзьями '
                    f'воспользуйся форматом: \n'
                    f'<i>/create_clan your_name</i> \n'
                    f'где name название будущего обьединения пример: \n'
                    f'<i>/create_clan Крутой_Чел</i>\n'
                    f'Стоимость создания обьединения 7500 очков')
not_in_clan = ('В данный момент ты не состоишь в объединении \n'
               'Чтобы вступить в объединение попроси команду у того кто в нем состоит\n'
               '\nВступить в обьединение можно с 10 уровня фабрики \n/create_clan чтобы создать объединение')


# @router.message(F.text.lower() == 'объединение')
@router.callback_query(F.data == 'open_clan')
async def clan_def(call: types.CallbackQuery):
    player = api.player(call.from_user.id)
    if player.clan_name == '':
        return await call.message.edit_text(not_in_clan, parse_mode='HTML', reply_markup=back_city)
    _text = f'🏆 *Лидеры Объединения \"{player.clan_name}\"* 🏆\n\n'
    _text += str(Leaderboard().Clan(player.clan_name))
    _text += f'💰Вклад в объединение {player.money:,}\n\n'
    if bool(player.clan_leader):
        _text += '👑*Вы основатель* этого объединения\n'

    _text += (f'\nПокинуть Объединение - */leave*'
              f'\nСсылка на вступление в объединение - `/join "{player.clan_name}"`')
    await call.message.edit_text(_text, parse_mode='Markdown', reply_markup=back_city)


@router.message(Command('leave'))
async def leave_clan_cm(message: types.Message):
    player = api.player(message.from_user.id)
    player.global_change({
        'telegram_id': message.from_user.id,
        'clan_name': '',
        'clan_leader': 0
    })
    await message.answer('Ты покинул обьединение')


@router.message(Command('join'))
async def join(message: types.Message):
    factory = api.factory(message.from_user.id)
    if factory.lvl < 10:
        return await message.answer(clan_lvl)
    try:
        name = message.text.split()[1]
    except:
        return await message.answer('Не указано название объединения для вступления')
    name = name.replace('"', '')
    player = api.player(message.from_user.id)
    if player.clan_name != '':
        return await message.answer('Вы уже в объединении')

    if not player.clan_exists(name):
        return await message.answer("Объединения не существует")

    player.clan_name = name
    await message.answer('Поздравляю вы в объединении')


@router.message(Command('create_clan'))
async def create_clan(message: types.Message):
    await message.answer('Функция временно недоступна')
    # factory = api.factory(message.from_user.id)
    # player = api.player(message.from_user.id)
    # if factory.lvl < 10:
    #     return await message.answer(clan_lvl)
    # try:
    #     clan_name = message.text.split()[1]
    # except:
    #     return await message.answer(create_clan_text, parse_mode='HTML')
    #
    # try:
    #     message.text.split()[2]
    # except:
    #     return await message.answer('Чтобы объединение состояло из несколких слов, заменяйте их на _')
    #
    # if not player.create_clan(clan_name):
    #     return await message.answer('Такое объединение уже существует')
    #
    # if len(clan_name) > 100:
    #     return await message.answer(create_clan_text, parse_mode='HTML')
    #
    # if player.clan_name != '':
    #     return await message.answer('Вы уже состоите в объединении')
    #
    # if player.money > 7500:
    #     player.money -= 7500
    #     player.clan_name = clan_name
    #     player.clan_leader = 1
    #     player.global_change({
    #         'telegram_id': message.from_user.id,
    #         'money': money,
    #     })
    #     await message.answer(f'Успешно создано обьединение {clan_name.replace('_', ' ')}')
    # else:
    #     await message.answer(not_enough_points)
