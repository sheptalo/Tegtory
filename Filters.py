import time

from aiogram.filters import BaseFilter
from aiogram import types

from bot import is_subscribed

last_button_click = 0
last_user = 0


class MenuFilter(BaseFilter):
    async def __call__(self, message: types.Message) -> bool:
        try:
            if message.text.lower() == 'меню' or message.text.lower() == 'предыдущая страница':
                return True
        except:
            return False


class SpamFilter(BaseFilter):
    async def __call__(self, message: types.Message) -> bool:
        global last_button_click, last_user
        try:
            if time.time() - last_button_click < 0.5 and last_user == message.from_user.id:
                return True
            else:
                last_user = message.from_user.id
                last_button_click = time.time()
        except:
            pass


class SpamFilterCallBack(BaseFilter):
    async def __call__(self, call: types.CallbackQuery) -> bool:
        global last_button_click, last_user
        try:
            if time.time() - last_button_click < 0.5 and last_user == call.from_user.id:
                return True
            else:
                last_user = call.from_user.id
                last_button_click = time.time()
        except:
            pass


class SubscribeFilter(BaseFilter):
    async def __call__(self, message: types.Message) -> bool:
        try:
            if not await is_subscribed(message.from_user.id):
                return True
        except:
            pass


class ProfileFilter(BaseFilter):
    async def __call__(self, message: types.Message) -> bool:
        try:
            if message.text is not None:
                return message.text.lower() == 'профиль' or message.text.upper() == 'Я'
            else:
                return False
        except:
            pass


class FarmFilter(BaseFilter):
    async def __call__(self, message: types.Message) -> bool:
        try:
            if message.text is not None:
                return message.text.lower() == 'ферма' or message.text.lower() == 'фарм'
            else:
                return False
        except:
            pass


class LeaderboardFilter(BaseFilter):
    async def __call__(self, message: types.Message) -> bool:
        try:
            if message.text is not None:
                return (message.text.lower() == 'таблица лидеров') or (message.text.upper() == 'ТЛ')
            else:
                return False
        except:
            pass
