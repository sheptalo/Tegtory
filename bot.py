from aiogram import Dispatcher, Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv
from mysql.connector import connect
import os
load_dotenv('.env')


dp = Dispatcher(storage=MemoryStorage())
bot = Bot(os.environ['BETA_API_TOKEN'], default=DefaultBotProperties(parse_mode='Markdown'))

con = connect(
        host=os.environ['DB_HOST'],
        port=3306,
        user=os.environ['USER_NAME'],
        password=os.environ['PASSWORD'],
        database=os.environ['DB_NAME'],
        autocommit=True
    )
cur = con.cursor(buffered=True)
