import random

from aioconsole import ainput

from bot import con, cur


async def console():
    inp = await ainput()
    while inp != 'exit':
        if inp == 'ping':
            con.ping(True)
            print('pinged')
        if inp == 'echo':
            print('echo')
        if inp == 'stock':
            new_price = random.randint(2, 8)
            cur.execute(f'UPDATE stock_price SET price = {new_price}')
            con.commit()
        if inp == 'eco':
            cur.execute('UPDATE Factory SET ecology = ecology - 1 WHERE ecology > 0')
            con.commit()

        inp = await ainput()



