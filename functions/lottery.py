import random

from bot import bot, api


async def lottery():
    win_tickets_bronze = ' '
    win_tickets_serebro = ' '
    win_tickets_gold = ' '
    win_tickets_stolar = ' '
    for i in range(100):
        win_tickets_bronze += f' {random.randint(1000, 1500)}'

    for i in range(1000):
        win_tickets_serebro += f' {random.randint(10000, 15000)}'

    for i in range(10000):
        win_tickets_gold += f' {random.randint(100000, 150000)}'

    for i in range(100000):
        win_tickets_stolar += f' {random.randint(1000000, 1500000)}'

    _user = await give_money_l(win_tickets_bronze, win_tickets_serebro, win_tickets_gold, win_tickets_stolar)
    await bot.send_message('@tegtory', 'Проходит розыгрыш билетов')

    for user in _user:
        api.player(str(user[1])).money += user[0]
        api.player(user[1]).stolar += user[3]
        await bot.send_message(user[1], f'Ваш билет {user[2]} выйграл')


async def give_money_l(bronze, serebro, gold, stolar):
    users = api.lottery_start()
    api.reset_tickets()
    won_user = []

    for user_id, ticket_ids in users:
        user_tickets = ticket_ids.split()
        for user_ticket in user_tickets:
            if user_ticket in bronze.split():
                user = [50000, user_id, user_ticket, 0]
                won_user.append(user)
            if user_ticket in serebro.split():
                if 1000000 <= int(user_ticket) <= 1500000:
                    stolar = 100
                user = [1000000, user_id, user_ticket, 0]
                won_user.append(user)
            if user_ticket in gold.split():
                user = [1000000000, user_id, user_ticket, 0]
                won_user.append(user)
            if user_ticket in stolar.split():
                user = [0, user_id, user_ticket, 100]
                won_user.append(user)

    return won_user
