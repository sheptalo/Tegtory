from aiogram import Dispatcher, Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage

from dotenv import load_dotenv
import os

from my_sin_api import SinApi

load_dotenv(".env")


dp = Dispatcher(storage=MemoryStorage())
bot = Bot(
    os.environ["API_TOKEN"],
    default=DefaultBotProperties(parse_mode="Markdown"),
)
api = SinApi(
    os.environ["DB_API_KEY"],
    os.environ["API_URL"] + "api/v1/",
    ssl_verify=False,
)
