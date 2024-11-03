from aiogram import Dispatcher, Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage

from dotenv import load_dotenv
import os
load_dotenv('.env')


dp = Dispatcher(storage=MemoryStorage())
bot = Bot(os.environ['API_TOKEN'], default=DefaultBotProperties(parse_mode='Markdown'))


