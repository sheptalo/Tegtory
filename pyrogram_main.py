from dotenv import load_dotenv
from pyrogram import Client
import os
load_dotenv('.env')

api_id = os.environ["API_ID"]
api_hash = os.environ["API_HASH"]
bot_token = os.environ['API_TOKEN']


async def get_chat_members(chat_id):
    app = Client("Имя | Бот", api_id=api_id, api_hash=api_hash, bot_token=bot_token, in_memory=True)
    chat_members = []
    await app.start()
    async for member in app.get_chat_members(chat_id):
        chat_members = chat_members + [member.user.id]
    await app.stop()
    return chat_members
