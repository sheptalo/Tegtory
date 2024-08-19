from aiogram import Dispatcher, Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv
from mysql.connector import connect
import os
load_dotenv('.env')


async def is_subscribed(user_id):
    chat_id = '@tegtory'
    try:

        chat_member = await bot.get_chat_member(chat_id, user_id)
        if chat_member.status == 'left':
            return False
        else:
            return True
    except:
        return False


dp = Dispatcher(storage=MemoryStorage())
bot = Bot(os.getenv('BETA_API_TOKEN'), default=DefaultBotProperties(parse_mode='Markdown'))

con = connect(
        host=os.getenv('DB_HOST'),
        port=3306,
        user=os.getenv('USER'),
        password=os.getenv('PASSWORD'),
        database=os.getenv('DB_NAME'),
        autocommit=True
    )
cur = con.cursor(buffered=True)
