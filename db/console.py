from aioconsole import ainput
from globalFunc.lottery import lottery


async def console():
    inp = await ainput()
    while inp != 'exit':
        from api import api
        if inp == 'stock':
            api.stock_update()
        if inp == 'eco':
            api.eco_update()
        if inp == 'league':
            api.league_update()
        if inp == 'lottery':
            await lottery()
        inp = await ainput()



