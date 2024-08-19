from bot import cur, con


async def give_money_l(bronze, serebro, gold, stolar):
    cur.execute('SELECT telegram_id, tickets FROM Users')
    a = cur.fetchall()
    cur.execute('UPDATE Users SET tickets = 0')
    con.commit()

    won_user = []

    for user_id, ticket_ids in a:
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
