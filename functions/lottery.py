import random

from bot import bot, api


async def lottery():
    bronze = set([str(random.randint(1000, 1500)) for _ in range(100)])
    serebro = set([str(random.randint(10000, 15000)) for _ in range(1000)])
    gold = set([str(random.randint(100000, 150000)) for _ in range(10000)])
    stolar = set([str(random.randint(1000000, 1500000)) for _ in range(1000)])

    message = await bot.send_message("@tegtory", "Проходит подсчет билетов!")
    results, total = await process_lottery(
        {i: 50000 for i in bronze},
        {i: 1000000 for i in serebro},
        {i: 1000000000 for i in gold},
        stolar,
    )

    for result in results:
        player = api.player(result.get("user_id"))
        player.set(
            {
                "money": player.money + result.get("money"),
                "stolar": player.stolar + result.get("stolar"),
            }
        )
        await bot.send_message(
            result.get("user_id"), f"Ваш билет {result.get('ticket')} выйграл"
        )
    amount = len(bronze) + len(serebro) + len(gold) + len(stolar)
    await message.edit_text(f"""
    Подсчет билетов прошел успешно
    
    Немного статистики:
    Всего билетов разыграно: {amount}
    Всего куплено: {total}
    
    купленых билетов победило: {len(results)}
    """)


async def process_lottery(bronze, serebro, gold, stolar):
    bronze.update(serebro)
    bronze.update(gold)

    win = bronze.copy()
    users = api.player(1).lottery_start()

    api.player(1).reset_tickets()
    results = []
    total = 0

    for uuid, tickets in users:
        user_tickets = tickets.split()
        total += len(user_tickets)
        for ticket in user_tickets:
            result = {
                "money": win.get(ticket, 0),
                "stolar": 0,
                "user_id": uuid,
                "ticket": ticket,
            }
            if ticket in stolar:
                result["stolar"] = 100

            if result["money"] > 0 or result["stolar"] > 0:
                results.append(result)

    return results, total
