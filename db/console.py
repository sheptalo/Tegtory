from aioconsole import ainput
from globalFunc.lottery import lottery


async def console():
    inp = await ainput()
    while inp != 'exit':
        if inp == 'lottery':
            await lottery()
        inp = await ainput()



